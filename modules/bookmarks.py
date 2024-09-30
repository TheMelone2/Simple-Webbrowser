from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def add_bookmark_current_tab(self):
    current_url = self.current_browser().url().toString()
    if not current_url.strip():
        self.show_error_message("Cannot add a blank bookmark.")
        return
    self.bookmarks.append(current_url)
    self.update_bookmark_menu()
    self.save_settings()
    self.open_settings()

def add_bookmark(self):
    url, ok = QInputDialog.getText(self, self.translate('Add Bookmark'), self.translate('URL') + ':')
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
        action.triggered.connect(lambda _, url=bookmark: self.current_browser().setUrl(QUrl(url)))
        self.bookmark_menu.addAction(action)
