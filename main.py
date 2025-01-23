import requests
from bs4 import BeautifulSoup
import re
import logging
from secret_loader import get_secrets
from translations import Translations

TEST = True
URL = "https://kouluruoka.fi/menu/helsinki_kapylanperuskouluhykkyla/"

FORBIDDEN_CHARACHTERS = ['&']

SECRETS = get_secrets()
translator = Translations()

if TEST:
    logging.basicConfig(
        filename="app.log",
        filemode="w",
        encoding='utf-8',
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.DEBUG
    )
else:
    logging.basicConfig(
        filename="app.log",
        filemode="a",
        encoding='utf-8',
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.INFO
    )

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
    logging.debug(f"Telegram message: {message}")
    # Check if the message was sent successfully
    if response.status_code == 200:
        logging.info("Message published successfully to instagram group: {group")
    else:
        logging.error("Failed to publish the message to instagram. Status code:", response.status_code)

# def clean_text(text):
#    return re.sub(r'\s*\([^)]*\)', '', text).strip()


def process_string(input_string:str) -> str:
    items = input_string.split('), ')
    processed_items = []

    for item in items:
        main_part, _, parentheses_part = item.partition('(')
        main_part = main_part.strip()

        if 'Veg' in parentheses_part:
            processed_items.append(f"{main_part}\U0001F33F")
        else:
            processed_items.append(main_part)

    return ', '.join(processed_items)

if __name__ == "__main__":
    # URL of the kouluruoka menu page

    # Send an HTTP GET request to the URL
    response = requests.get(URL)
    logging.debug(f"response: {response}")
    # Check if the request was successful
    if response.status_code != 200:
        logging.warning(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        exit(1)

    # Parse the HTML content using BeautifulSoup
    soup:BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
    # Find all day menu items
    logging.debug(f"soup: {soup}")
    # print(soup)
    school = soup.find('h1', id='pageTitle').get_text(strip=True)
    logging.debug(f"school:{school}")
    #print(f"school: {school}")
    message = ""
    # Extract lunch options for each day
    articles = soup.find_all('article')
    #print(articles)

    for article in articles:
        # Extract the day title from <h2> tag
        day_title = article.find('h2').text

        # Find all div elements that are direct children of the article
        div_elements = article.find_all('div', recursive=False)

        # Extract the Lounas items and save them as items
        items = []
        for div in div_elements:
            span = div.find('span')
            if span:
                # Appends the text of the span to the items list.
                items.append(span.text)

        # Print the extracted items
        lunch_options = ""
        for item in items:
            # print(item)
            lunch_options += f"\n\u2022{process_string(item)}"

        # break

        # Print the extracted values
        #print("Day Title:", day_title)
        #print("Lunch option:", lunch_options)

        message += f"<u>{day_title}</u>{lunch_options}\n"
    message = remove_forbidden_characters(message, FORBIDDEN_CHARACHTERS)

    # Add translations
    message = translator.get_translated_message(message=message)

    message = f"{school}\n{message}"
    logging.info(message)
    logging.info(f"Telegram message prepared for {school}")

    send_telegram(message)

