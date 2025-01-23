import requests
from bs4 import BeautifulSoup


def extract_headings(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all h2, h3, and h4 tags
        headings = soup.find_all(['h2', 'h4'])

        # Extract and print the text from each heading
        for heading in headings:
            if heading.name == "h2":
                print (f"\n")
            print(f"{heading.text.strip()}")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")



url = "https://kouluruoka.fi/menu/helsinki_kapylanperuskouluhykkyla/"  # Replace with the actual URL you want to scrape
extract_headings(url)