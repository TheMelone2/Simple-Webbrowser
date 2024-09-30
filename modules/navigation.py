from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# def current_browser(main_window):
  #  return main_window.tabs.currentWidget().findChild(QWebEngineView)

def current_browser(main_window):
    current_index = main_window.tabs.currentIndex()
    print(f"Current Index: {current_index}")
    if current_index != -1:
        browser = main_window.tabs.widget(current_index)
        print(f"Returning Browser: {browser}")
        return browser
    return None

      

def current_browser_back(main_window):
    browser = current_browser(main_window)
    if browser:
        browser.back()

def current_browser_forward(main_window):
    browser = current_browser(main_window)
    if browser:
        browser.forward()

def current_browser_reload(main_window):
    browser = current_browser(main_window)
    if browser:
        browser.reload()

def navigate_to_url(main_window):
    url = main_window.url_bar.text()
    if not url.startswith('http://') and not url.startswith('https://') and not url.startswith('www.'):
        url = 'http://' + url
    browser = current_browser(main_window)
    if browser:
        qurl = QUrl(url)
        browser.setUrl(qurl)
        main_window.update_history(qurl, main_window.SEARCH_ENGINES)

def update_url_bar(main_window, url):
    main_window.url_bar.setText(url)


def update_tab_title(main_window):
    browser = current_browser(main_window)
    if browser:
        main_window.tabs.setTabText(main_window.tabs.currentIndex(), browser.title())
