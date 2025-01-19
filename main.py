import requests
from bs4 import BeautifulSoup
import re
import logging

forbidden_characters = ['&']

TEST = False

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
def remove_forbidden_characters(input_string, forbidden_characters):
    return ''.join([char for char in input_string if char not in forbidden_characters])


def send_telegram(message):
    # Your bot token
    TOKEN = '7716411342:AAEjzGb-c5xMSPvcOpPbsdUwTXBwjcAqzrw'
    # Your chat ID
    CHAT_ID = '5963518143' # DM
    CHAT_ID = "-1002362564209" # group Kouluruoka Hykkylä
    group = "Kouluruoka Hykkylä"
    # URL for sending the message
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
     # https://api.telegram.org/bot7716411342:AAEjzGb-c5xMSPvcOpPbsdUwTXBwjcAqzrw/sendMessage?chat_id=335513962&text="Hello, this is a message from the bot"
    logging.debug(f"Telegram message: {message}")
    # Send the request
    response = requests.get(url)
    # Check if the message was sent successfully
    if response.status_code == 200:
        logging.info("Message published successfully to instagram group: {group")
    else:
        logging.error("Failed to publish the message to instagram. Status code:", response.status_code)

def clean_text(text):
    return re.sub(r'\s*\([^)]*\)', '', text).strip()


def process_string(input_string):
    items = input_string.split('), ')
    processed_items = []

    for item in items:
        main_part, _, parentheses_part = item.partition('(')
        main_part = main_part.strip()

        if 'Veg' in parentheses_part:
            processed_items.append(f"{main_part} [V]")
        else:
            processed_items.append(main_part)

    return ', '.join(processed_items)


# URL of the kouluruoka menu page
url = "https://kouluruoka.fi/menu/helsinki_kapylanperuskouluhykkyla/"
# Send an HTTP GET request to the URL
response = requests.get(url)
logging.debug(f"response: {response}")
# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all day menu items
    logging.debug(f"soup: {soup}")
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
        div_elements = soup.article.find_all('div', recursive=False)

        # Extract the Lounas items and save them as items
        items = []
        for div in div_elements:
            span = div.find('span')
            if span:
                items.append(span.text)

        # Print the extracted items
        lunch_options = ""
        for item in items:
            # print(item)
            lunch_options += f"\n**{process_string(item)}"

        # break

        # Print the extracted values
        #print("Day Title:", day_title)
        #print("Lunch option:", lunch_options)

        message += f"{day_title}{lunch_options}\n\n"
        message = remove_forbidden_characters(message, forbidden_characters)

    message = f"{school}\n{message}"
    print(message)
    logging.info(f"Telegram message prepared for {school}")

    send_telegram(message)
else:
    logging.warning(f"Failed to retrieve the webpage. Status code: {response.status_code}")