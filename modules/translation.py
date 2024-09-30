import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def load_translations(self):
    try:
        with open('translations.json', 'r') as file:
            self.translations = json.load(file)
    except FileNotFoundError:
        self.translations = {}

def translate(self, text):
    lang = self.current_language
    return self.translations.get(lang, {}).get(text, text)

def change_language(self):
    self.current_language = self.language_combobox.currentText()
    self.load_translations()
    self.open_settings()
