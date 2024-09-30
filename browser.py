import sys
import json
import traceback
import requests
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from datetime import datetime

from modules.shortcuts import setup_shortcuts

from modules.translation import load_translations, translate

from modules.bookmarks import (
    add_bookmark_current_tab,
    update_bookmark_menu,
    remove_bookmark,
    add_bookmark
)
from modules.history import update_history, load_history, open_history

from modules.navigation import (
    current_browser,
    current_browser_back,
    current_browser_forward,
    current_browser_reload,
    navigate_to_url,
    update_url_bar,
    update_tab_title
)
from modules.settings import (
    load_settings,
    save_settings,
    open_settings,
    change_search_engine,
    toggle_palette,
    change_language,
    update_palette
)
from modules.tabs import (
    add_tab,
    close_tab,
    update_current_tab
)

from modules.search import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.SEARCH_ENGINES = {
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

        translations = load_translations(self)
        load_settings(self)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setTabBar(TabBar(self))
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction(QIcon.fromTheme('go-previous'), translate(self, 'Back'), self)
        back_btn.setToolTip(translate(self, 'Back'))
        back_btn.triggered.connect(lambda: current_browser_back(self))
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon.fromTheme('go-next'), translate(self, 'Forward'), self)
        forward_btn.setToolTip(translate(self, 'Forward'))
        forward_btn.triggered.connect(lambda: current_browser_forward(self))
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon.fromTheme('view-refresh'), translate(self, 'Reload'), self)
        reload_btn.setToolTip(translate(self, 'Reload'))
        reload_btn.triggered.connect(lambda: current_browser_reload(self))
        navbar.addAction(reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(lambda: navigate_to_url(self))
        self.url_bar.textChanged.connect(lambda url: update_url_bar(self, url))
        navbar.addWidget(self.url_bar)

        self.search_engine_menu = QMenu(translate(self, 'Search Engine'), self)
        self.search_engine_btn = navbar.addAction(QIcon.fromTheme('search'), translate(self, 'Search Engine'))
        self.search_engine_btn.setMenu(self.search_engine_menu)

        self.bookmark_menu = QMenu(translate(self, 'Bookmarks'), self)
        self.bookmark_btn = navbar.addAction(QIcon.fromTheme('bookmark-new'), translate(self, 'Bookmarks'))
        self.bookmark_btn.setMenu(self.bookmark_menu)

        history_btn = QAction(QIcon.fromTheme('history'), translate(self, 'History'), self)
        history_btn.triggered.connect(lambda: open_history(self))
        navbar.addAction(history_btn)

        settings_btn = QAction(QIcon.fromTheme('preferences-system'), translate(self, 'Settings'), self)
        settings_btn.triggered.connect(lambda: open_settings(self))
        navbar.addAction(settings_btn)

        add_tab(self)

        update_search_engine_menu(self)
        update_bookmark_menu(self)

        self.tabs.currentChanged.connect(lambda: update_current_tab(self))
        current_browser(self).loadFinished.connect(lambda: update_tab_title(self))

        update_palette(self)

        setup_shortcuts(self)

    def open_credits(self):
        credits_dialog = QDialog(self)
        credits_dialog.setWindowTitle(self.translate('Credits'))
        credits_dialog.setFixedSize(300, 200)

        layout = QVBoxLayout()
        credits_label = QLabel(self.translate('Credits') + ':')
        layout.addWidget(credits_label)

        credits_text = QTextEdit()
        credits_text.setReadOnly(True)
        # developer: themelon
        credits_text.setPlainText(self.translate('Developer') + ': themelon\n' +
                                    self.translate('Icons') + ': KDE\n' +
                                    self.translate('Search Engines') + ': ' + ', '.join(self.SEARCH_ENGINES.keys()))
        layout.addWidget(credits_text)

        credits_dialog.setLayout(layout)
        credits_dialog.exec_()

    def some_method(self, url):
        update_history(self, url, self.SEARCH_ENGINES)

    load_settings = load_settings
    save_settings = save_settings
    load_translations = load_translations
    translate = translate
    add_bookmark_current_tab = add_bookmark_current_tab
    show_error_message = QMessageBox.critical
    add_tab = add_tab
    close_tab = close_tab
    update_current_tab = update_current_tab
    update_tab_title = update_tab_title
    current_browser = current_browser
    current_browser_back = current_browser_back
    current_browser_forward = current_browser_forward
    current_browser_reload = current_browser_reload
    navigate_to_url = navigate_to_url
    update_url_bar = update_url_bar
    update_history = update_history
    open_history = open_history
    update_palette = update_palette
    open_settings = open_settings
    change_search_engine = change_search_engine
    toggle_palette = toggle_palette
    add_bookmark = add_bookmark
    remove_bookmark = remove_bookmark
    update_bookmark_menu = update_bookmark_menu
    update_search_engine_menu = update_search_engine_menu
    set_search_engine = update_search_engine_menu
    change_language = change_language


class TabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setExpanding(False)
        self.setTabsClosable(True)

        self.addTabButton = QPushButton('+')
        self.addTabButton.setFixedSize(30, 30)
        self.addTabButton.setToolTip('Tab erstellen')
        self.addTabButton.clicked.connect(self.add_new_tab)
        self.setTabButton(self.count(), QTabBar.RightSide, self.addTabButton)

    def add_new_tab(self):
        if self.parent() and isinstance(self.parent(), MainWindow):
            add_tab(self.parent())

    def tabCloseRequested(self, index):
        if self.parent() and isinstance(self.parent(), MainWindow):
            close_tab(self.parent(), index)

        if self.count() == 1:
            self.setTabButton(self.count() - 1, QTabBar.RightSide, None)
        else:
            self.setTabButton(self.count() - 1, QTabBar.RightSide, self.addTabButton)



def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    log_message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(log_message)
    
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(log_message)
    
    show_crash_popup(log_message)

def show_crash_popup(log_message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText("Your client has crashed. Log files are in PATH-TO-LOG. If this keeps happening, please contact us here.")
    msg_box.setWindowTitle("Client Crash")
    msg_box.setStandardButtons(QMessageBox.Open | QMessageBox.Ignore)
    
    button_open = msg_box.button(QMessageBox.Open)
    button_open.setText("Open Log File")
    
    button_ignore = msg_box.button(QMessageBox.Ignore)
    button_ignore.setText("Ignore and Restart")
    
    ret = msg_box.exec_()
    
    if ret == QMessageBox.Open:
        os.startfile(LOG_FILE_PATH)
    elif ret == QMessageBox.Ignore:
        restart_client()

LOG_FILE_PATH = "client.log"

if not os.path.exists(LOG_FILE_PATH):
    with open(LOG_FILE_PATH, "w") as log_file:
        log_file.write("")
else:
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write("\n\n")

def restart_client():
    QProcess.startDetached(sys.executable, sys.argv)
    sys.exit()

sys.excepthook = handle_exception

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        QApplication.setApplicationName('Simple Browser')
        window = MainWindow()
        window.show()
        app.exec_()
    except Exception as e:
        handle_exception(*sys.exc_info())
