from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

SEARCH_ENGINES = {
    'Ecosia': 'https://www.ecosia.org',
    'Google': 'https://www.google.com',
    'Bing': 'https://www.bing.com',
    'DuckDuckGo': 'https://www.duckduckgo.com',
    'Brave': 'https://search.brave.com',
    'Qwant': 'https://www.qwant.com',
    'Startpage': 'https://www.startpage.com',
    'Yahoo': 'https://search.yahoo.com',
    'Yandex': 'https://www.yandex.com'
}

def set_search_engine(self, url):
    self.selected_search_engine = [key for key, value in SEARCH_ENGINES.items() if value == url][0]
    self.start_url = url
    self.save_settings()
    self.current_browser().setUrl(QUrl(self.start_url))
    self.update_search_engine_menu()

def update_search_engine_menu(self):
    self.search_engine_menu.clear()
    for engine, url in SEARCH_ENGINES.items():
        action = QAction(engine, self)
        action.setCheckable(True)
        action.setChecked(url == self.start_url)
        action.triggered.connect(lambda _, url=url: self.set_search_engine(url))
        self.search_engine_menu.addAction(action)
