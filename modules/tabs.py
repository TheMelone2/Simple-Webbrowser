from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def add_tab(self, url=None, label=None):
    label = label or self.translate('New Tab')
    browser = QWebEngineView()
    browser.setUrl(QUrl(url or self.start_url))
    index = self.tabs.addTab(browser, label)
    self.tabs.setCurrentIndex(index)
    self.update_tab_title()
    browser.iconChanged.connect(lambda: self.tabs.setTabIcon(index, browser.icon()))

def close_tab(self, index):
    if self.tabs.count() > 1:
        self.tabs.removeTab(index)
    else:
        QMessageBox.warning(self, self.translate('Warning'), self.translate('Last Tab Warning'))

def update_current_tab(self):
    self.update_url_bar(self.current_browser().url().toString())
    self.update_tab_title()
    self.tabs.currentWidget().iconChanged.connect(lambda: self.tabs.setTabIcon(self.tabs.currentIndex(), self.tabs.currentWidget().icon()))

def update_tab_title(self):
    current_browser = self.current_browser()
    if current_browser:
        title = current_browser.page().title()
        index = self.tabs.currentIndex()
        self.tabs.setTabText(index, title if title else self.translate('New Tab'))

def current_browser(self):
    index = self.tabs.currentIndex()
    return self.tabs.widget(index)
