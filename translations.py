import json
import re


class Translations:
    def __init__(self):
        self.path:str = "config/translations.json"
        self.translation_list:dict = self.get_translation_dict()

    # def get_translation(self, key:str) -> str:
    #     if key not in self.translation_list:
    #         # Key not found in translation list
    #         return key
    #
    #     return self.translation_list[key]

    def get_translated_message(self, message:str) -> str:
        # # Split the message into words
        # words = message.split()
        #
        # # Translate each word if it's in the dictionary
        # translated_words = [self.translation_list.get(word, word) for word in words]
        #
        # # Join the words back into a sentence
        # return ' '.join(translated_words)


        def translate_word(match):
            word = match.group(0)
            return self.translation_list.get(word, word)
        # Use regex to match words, preserving all whitespace
        return re.sub(r'\S+', translate_word, message)

    def get_translation_dict(self) -> dict:
        with open(file="config/translations.json", mode="r") as file:
            return json.load(file)