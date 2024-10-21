import requests
from bs4 import BeautifulSoup
import re
import logging

forbidden_characters = ['&']

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


# URL of the kouluruoka menu page
url = "https://kouluruoka.fi/menu/helsinki_kapylanperuskouluhykkyla/"
# Send an HTTP GET request to the URL
response = requests.get(url)
# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all day menu items
    day_menus = soup.find_all(class_="menu-module--dayMenu--eb50b")
    school = soup.find('h1', id='pageTitle').get_text(strip=True)
    #print(f"school: {school}")
    message = ""
    # Extract lunch options for each day
    for day_menu in day_menus:
        day_title = day_menu.find('h2').string.strip()
        lunch_options = day_menu.find_all('h3', string=lambda t: t and 'Lounas' in t)
        lunch = ""
        #print(f"**{day_title}**")
        for lunch_option in lunch_options:
            lunch_details = lunch_option.find_next('div').get_text(strip=True)

            lunch_details = lunch_details.replace("Veg", ")[V](")
            lunch_details = re.sub(r'\(.*?\)', '', lunch_details)
            #print(lunch_details)
            lunch += f"**{lunch_details}\n"
        message += f"{day_title}\n{lunch}\n"
        message = remove_forbidden_characters(message, forbidden_characters)

    message = f"{school}\n{message}"
    logging.info(f"Telegram message prepared for {school}")

    send_telegram(message)
else:
    logging.warning(f"Failed to retrieve the webpage. Status code: {response.status_code}")