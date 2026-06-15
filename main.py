import requests
from bs4 import BeautifulSoup
from secret_loader import get_secrets
from translations import Translations
from pathlib import Path
from logging_config import setup_uniform_logging  # ← Lokaal in kouluruoka/

test = True
logger = setup_uniform_logging("kouluruoka", test=test)  # ← 1 regel!

test = True
URL = "https://kouluruoka.fi/menu/helsinki_kapylanperuskouluhykkyla/"
FORBIDDEN_CHARACHTERS = ['&']
SECRETS = get_secrets()
translator = Translations()


# Function to remove forbidden characters using list comprehension
def remove_forbidden_characters(input_string:str, forbidden_characters:list) -> str:
    return ''.join([char for char in input_string if char not in forbidden_characters])


def send_telegram(message:str) -> None:
    """
    Send the main message through telegram
    :param message:
    :return:
    """
    # Your bot token
    TOKEN = SECRETS["TOKEN"]
    # Your chat ID
    CHAT_ID = SECRETS["CHAT_ID"]
    # group = "Kouluruoka Hykkylä"
    # url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    # https://api.telegram.org/bot7716411342:AAEjzGb-c5xMSPvcOpPbsdUwTXBwjcAqzrw/sendMessage?chat_id=335513962&text = "Hello, this is a message from the bot"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    # Prepare the parameters
    params = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    # Send the request
    response = requests.get(url, params=params)
    logger.debug(f"Telegram message: {message}")
    # Check if the message was sent successfully
    if response.status_code == 200:
        logger.info("Message published successfully to instagram group: {group")
    else:
        logger.error("Failed to publish the message to instagram. Status code:", response.status_code)

# def clean_text(text):
#    return re.sub(r'\s*\([^)]*\)', '', text).strip()


def remove_parantheses(input_string:str) -> str:
    items = input_string.split('), ')
    processed_items = []

    for item in items:
        main_part, _, parentheses_part = item.partition('(')
        main_part = main_part.strip()

        if 'Veg' in parentheses_part:
            processed_items.append(f"{main_part} \U0001F33F")
        else:
            processed_items.append(main_part)

    return ', '.join(processed_items)

def fetch_and_parse_webpage(url:str) -> BeautifulSoup:
    """
    Fetches a webpage and parses its content using BeautifulSoup.

    Args:
    url (str): The URL of the webpage to fetch.

    Returns:
    BeautifulSoup: A BeautifulSoup object containing the parsed HTML content.

    Raises:
    SystemExit: If the webpage cannot be retrieved (non-200 status code).
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        #logger.debug(f"Response: {response}")

        # Check if the request was successful
        if response.status_code != 200:
            logger.warning(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            raise SystemExit(1)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        #logger.debug(f"Soup: {soup}")

        return soup

    except requests.RequestException as e:
        logger.error(f"An error occurred while fetching the webpage: {e}")
        raise SystemExit(1)

# Example usage:
# URL = "https://example.com"
# soup = fetch_and_parse_webpage(URL)
# Now you can use 'soup' to further process the webpage content


if __name__ == "__main__":
    # URL of the kouluruoka menu page
    soup = fetch_and_parse_webpage(URL)

    schoolName = soup.find('h1', id='pageTitle').get_text(strip=True)
    logger.debug(f"school:{schoolName}")

    # Extract lunch options for each day
    articles = soup.find_all('article')

    # --- CHECK 1: If no article tags exist at all ---
    if not articles:
        logger.info(f"No content found for {schoolName}. Skipping Telegram notification (likely a holiday).")
        exit(0)

    message_body = ""

    for article in articles:
        day_title = article.find('h2').get_text(strip=True)

        items = []
        # Inspect top-level divs to find the one with h3 containing "Lounas"
        for div in article.find_all('div', recursive=False):
            h3 = div.find('h3')
            if h3 and 'Lounas' in h3.get_text():
                menu_div = h3.find_next_sibling('div')
                if menu_div:
                    span = menu_div.find('span')
                    if span:
                        items.append(span.get_text(strip=True))

        lunch_options = ""
        for item in items:
            lunch_options += f"\n\u2022{remove_parantheses(item)}"

        # Only add the day to the message if it actually has lunch items listed
        if lunch_options.strip():
            message_body += f"<u>{day_title}</u>{lunch_options}\n"

    # --- CHECK 2: If articles exist but they are all completely empty ---
    if not message_body.strip():
        logger.info(f"Menu articles are empty for {schoolName}. Skipping Telegram notification due to holidays.")
        exit(0)

    # Remove characters like & as they create an error in the telegram message
    message_body = remove_forbidden_characters(message_body, FORBIDDEN_CHARACHTERS)

    # Add translations
    message_body = translator.get_translated_message(message=message_body)

    # Combine school name with the verified message content
    final_message = f"{schoolName}\n{message_body}"

    logger.info(f"Telegram message prepared for {schoolName}")
    send_telegram(final_message)