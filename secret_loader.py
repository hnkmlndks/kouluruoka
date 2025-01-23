import json

def get_secrets() -> dict:
    with open(file="config/secrets.json", mode="r") as jsonfile:
        return json.load(jsonfile)