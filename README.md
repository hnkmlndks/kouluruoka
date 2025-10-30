
# 🛰️ School Menu Telegram Bot

This Python script fetches the lunch menu from a specific school website, processes the data, translates it, and sends the result via Telegram.

## 🧪 Features

- Connects to [kouluruoka.fi](https://kouluruoka.fi/menu/helsinki_kapylanperuskouluhykkyla/)
- Parses HTML using BeautifulSoup
- Removes unwanted characters like `&amp;`
- Detects vegetarian meals and adds a 🌿 icon
- Translates the message using an external `Translations` class
- Sends the message via Telegram using a bot
- Logs all steps to `app.log`

## 📦 Requirements

- Python 3.7+
- `requests`
- `beautifulsoup4`
- `logging`
- `secret_loader.py` file with `get_secrets()` function
- `translations.py` file with `Translations` class

Install required packages:
```bash
pip install requests beautifulsoup4
```

## 🔧 Configuration

Make sure you have a `secret_loader.py` file with:
```python
SECRETS = {
    "TOKEN": "<your_bot_token>",
    "CHAT_ID": "<your_chat_id>"
}
```

## ▶️ Usage

Run the script:
```bash
python scriptname.py
```

The script will fetch the menu, process it, and send it via Telegram to the specified chat.

## 🛠️ Debugging

If `TEST = True`, logging is set to DEBUG level and `app.log` is overwritten on each run.

## 📄 License

Free to use and modify for personal purposes.
