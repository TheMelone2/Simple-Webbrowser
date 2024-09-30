from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage

def setup_shortcuts(self):
    new_tab_shortcut = QShortcut(QKeySequence('Ctrl+N'), self)
    new_tab_shortcut.activated.connect(self.add_tab)
    
    history_shortcut = QShortcut(QKeySequence('Ctrl+H'), self)
    history_shortcut.activated.connect(self.open_history)
    
    settings_shortcut = QShortcut(QKeySequence('Ctrl+E'), self)
    settings_shortcut.activated.connect(self.open_settings)
    
    bookmark_shortcut = QShortcut(QKeySequence('Ctrl+B'), self)
    bookmark_shortcut.activated.connect(self.add_bookmark)
    
    bookmark_current_tab_shortcut = QShortcut(QKeySequence('Ctrl+Shift+B'), self)
    bookmark_current_tab_shortcut.activated.connect(self.add_bookmark_current_tab)
    
    # Developer Tools    
    def open_dev_tools():
        print("Dev Tools Shortcut Triggered")
        browser = self.current_browser()
        if browser:
            if isinstance(browser, QWebEngineView):
                page = browser.page()
                if page:
                    print("Triggering InspectElement")
                    page.triggerAction(QWebEnginePage.InspectElement)
                else:
                    print("Error: Page is None")
            else:
                print("Error: Browser is not a QWebEngineView")
        else:
            print("Error: Browser is None")

    dev_tools_shortcut = QShortcut(QKeySequence('Ctrl+Shift+I'), self)
    dev_tools_shortcut.activated.connect(open_dev_tools)