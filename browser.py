import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from datetime import datetime

SEARCH_ENGINES = {
    'Ecosia': 'https://www.ecosia.org',
    'Google': 'https://www.google.com',
    'Bing': 'https://www.bing.com',
    'DuckDuckGo': 'https://www.duckduckgo.com',
    'Brave': 'https://search.brave.com'
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.load_settings()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(self.start_url)) 

        self.setCentralWidget(self.browser)

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction(QIcon.fromTheme('go-previous'), 'Zurück', self)
        back_btn.setToolTip('Zurück')
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon.fromTheme('go-next'), 'Vorwärts', self)
        forward_btn.setToolTip('Vorwärts')
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon.fromTheme('view-refresh'), 'Neu laden', self)
        reload_btn.setToolTip('Neu laden')
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.search_engine_menu = QMenu('Suchmaschine', self)
        self.search_engine_btn = navbar.addAction(QIcon.fromTheme('search'), 'Suchmaschine')
        self.search_engine_btn.setMenu(self.search_engine_menu)
        self.update_search_engine_menu()

        self.bookmark_menu = QMenu('Lesezeichen', self)
        self.bookmark_btn = navbar.addAction(QIcon.fromTheme('bookmark-new'), 'Lesezeichen')
        self.bookmark_btn.setMenu(self.bookmark_menu)
        self.update_bookmark_menu()

        history_btn = QAction(QIcon.fromTheme('history'), 'Verlauf', self)
        history_btn.triggered.connect(self.open_history)
        navbar.addAction(history_btn)

        settings_btn = QAction(QIcon.fromTheme('preferences-system'), 'Einstellungen', self)
        settings_btn.triggered.connect(self.open_settings)
        navbar.addAction(settings_btn)

        self.update_palette()

        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadFinished.connect(self.update_title)
        self.browser.urlChanged.connect(self.update_history)

    def update_search_engine_menu(self):
        self.search_engine_menu.clear()
        for engine, url in SEARCH_ENGINES.items():
            action = QAction(engine, self)
            action.setCheckable(True)
            action.setChecked(url == self.start_url)
            action.triggered.connect(lambda _, url=url: self.set_search_engine(url))
            self.search_engine_menu.addAction(action)

    def set_search_engine(self, url):
        self.selected_search_engine = [key for key, value in SEARCH_ENGINES.items() if value == url][0]
        self.start_url = url
        self.save_settings()
        self.browser.setUrl(QUrl(self.start_url))
        self.update_search_engine_menu()

    def navigate_to_url(self):
        text = self.url_bar.text()
        if text.startswith('http://') or text.startswith('https://'):
            self.browser.setUrl(QUrl(text))
        else:
            search_url = f"{self.start_url}/search?q={text}"
            self.browser.setUrl(QUrl(search_url))
        self.update_history(self.browser.url())

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def update_history(self, url):
        url_str = url.toString()
        try:
            with open('history.json', 'r') as file:
                history = json.load(file)
        except FileNotFoundError:
            history = []

        history.append({'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'url': url_str})

        with open('history.json', 'w') as file:
            json.dump(history, file, indent=4)

    def load_history(self):
        try:
            with open('history.json', 'r') as file:
                history = json.load(file)
                return history
        except FileNotFoundError:
            return []

    def open_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle('Verlauf')
        history_dialog.setFixedSize(400, 300)

        layout = QVBoxLayout()

        history_list = QListWidget()
        history_data = self.load_history()
        for entry in history_data:
            item_text = f"{entry['timestamp']} - {entry['url']}"
            history_list.addItem(item_text)

        layout.addWidget(history_list)

        history_dialog.setLayout(layout)
        history_dialog.exec_()

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(title + ' - Simple Browser')

    def update_palette(self):
        palette = QPalette()
        if self.current_palette == 'dark':
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
            palette.setColor(QPalette.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
        else:
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
            palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
            palette.setColor(QPalette.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(0, 0, 255))
        self.setPalette(palette)

    def open_settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle('Einstellungen')
        settings_dialog.setFixedSize(400, 300)

        layout = QVBoxLayout()

        search_engine_label = QLabel('Suchmaschine:')
        layout.addWidget(search_engine_label)

        self.search_engine_combobox = QComboBox()
        self.search_engine_combobox.addItems(SEARCH_ENGINES.keys())
        self.search_engine_combobox.setCurrentText(self.selected_search_engine)
        self.search_engine_combobox.currentIndexChanged.connect(self.change_search_engine)
        layout.addWidget(self.search_engine_combobox)

        mode_toggle = QPushButton('Wechseln zu ' + ('Hellmodus' if self.current_palette == 'dark' else 'Dunkelmodus'))
        mode_toggle.clicked.connect(self.toggle_palette)
        layout.addWidget(mode_toggle)

        bookmark_layout = QVBoxLayout()
        bookmark_layout.addWidget(QLabel('Lesezeichen:'))

        self.bookmark_list = QListWidget()
        for bookmark in self.bookmarks:
            self.bookmark_list.addItem(bookmark)
        bookmark_layout.addWidget(self.bookmark_list)

        add_bookmark_btn = QPushButton('Lesezeichen hinzufügen')
        add_bookmark_btn.clicked.connect(self.add_bookmark)
        bookmark_layout.addWidget(add_bookmark_btn)

        remove_bookmark_btn = QPushButton('Lesezeichen entfernen')
        remove_bookmark_btn.clicked.connect(self.remove_bookmark)
        bookmark_layout.addWidget(remove_bookmark_btn)

        layout.addLayout(bookmark_layout)

        settings_dialog.setLayout(layout)
        settings_dialog.exec_()

    def change_search_engine(self):
        self.selected_search_engine = self.search_engine_combobox.currentText()
        self.start_url = SEARCH_ENGINES[self.selected_search_engine]
        self.set_search_engine(self.start_url)
        self.save_settings()
        self.update_search_engine_menu()

    def toggle_palette(self):
        self.current_palette = 'light' if self.current_palette == 'dark' else 'dark'
        self.update_palette()
        self.save_settings()
        self.open_settings()

    def add_bookmark(self):
        url, ok = QInputDialog.getText(self, 'Lesezeichen hinzufügen', 'URL:')
        if ok and url:
            self.bookmarks.append(url)
            self.update_bookmark_menu()
            self.save_settings()
            self.open_settings()

    def remove_bookmark(self):
        selected_items = self.bookmark_list.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            self.bookmarks.remove(item.text())
        self.update_bookmark_menu()
        self.save_settings()
        self.open_settings()

    def update_bookmark_menu(self):
        self.bookmark_menu.clear()
        for bookmark in self.bookmarks:
            action = QAction(bookmark, self)
            action.triggered.connect(lambda _, url=bookmark: self.browser.setUrl(QUrl(url)))
            self.bookmark_menu.addAction(action)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as file:
                settings = json.load(file)
                self.bookmarks = settings.get('bookmarks', [])
                self.current_palette = settings.get('palette', 'dark')
                self.selected_search_engine = settings.get('search_engine', 'Ecosia')
                self.start_url = SEARCH_ENGINES[self.selected_search_engine]
        except FileNotFoundError:
            self.bookmarks = []
            self.current_palette = 'dark'
            self.selected_search_engine = 'Ecosia'
            self.start_url = SEARCH_ENGINES[self.selected_search_engine]

    def save_settings(self):
        settings = {
            'bookmarks': self.bookmarks,
            'palette': self.current_palette,
            'search_engine': self.selected_search_engine
        }
        with open('settings.json', 'w') as file:
            json.dump(settings, file, indent=4)

app = QApplication(sys.argv)
QApplication.setApplicationName('Simple Browser')
window = MainWindow()
window.show()
app.exec_()
