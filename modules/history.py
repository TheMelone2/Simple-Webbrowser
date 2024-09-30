import json
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def is_search_engine_url(url, search_engines):
    """
    Check if the given URL is a search engine query.
    This uses a more flexible approach to match URLs that may contain search parameters.
    """
    for engine_url in search_engines.values():
        if engine_url in url:  # Check if search engine base URL is in the current URL
            return True
    return False

def update_history(main_window, url, search_engines):
    if isinstance(url, QUrl):
        url_str = url.toString()
    else:
        url_str = url
        
    try:
        with open('history.json', 'r') as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []
    
    # Use the improved search check
    is_search = is_search_engine_url(url_str, search_engines)
    
    # Append new history entry
    history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'url': url_str,
        'search': is_search
    })
    
    with open('history.json', 'w') as file:
        json.dump(history, file, indent=4)

def load_history():
    try:
        with open('history.json', 'r') as file:
            history = json.load(file)
            return history
    except FileNotFoundError:
        return []

def clear_history():
    with open('history.json', 'w') as file:
        json.dump([], file)

def open_clear_history_dialog(main_window):
    clear_dialog = QMessageBox(main_window)
    clear_dialog.setWindowTitle(main_window.translate('Clear history'))
    clear_dialog.setText(main_window.translate('Are you sure you want to clear the history?'))
    clear_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    clear_dialog.setDefaultButton(QMessageBox.No)
    
    def on_button_clicked(button):
        if clear_dialog.buttonRole(button) == QMessageBox.YesRole:
            clear_history()
    
    clear_dialog.buttonClicked.connect(on_button_clicked)
    clear_dialog.exec_()
    
def open_export_history_dialog(main_window):
    export_dialog = QFileDialog(main_window)
    export_dialog.setWindowTitle(main_window.translate('Export history'))
    export_dialog.setAcceptMode(QFileDialog.AcceptSave)
    export_dialog.setNameFilter(main_window.translate('JSON files (*.json)'))
    export_dialog.setDefaultSuffix('json')
    export_dialog.selectFile('history.json')
    export_dialog.fileSelected.connect(lambda path: export_history(path))
    export_dialog.exec_()
    
def export_history(path):
    with open('history.json', 'r') as file:
        history = json.load(file)
    with open(path, 'w') as file:
        json.dump(history, file, indent=4)
        
def open_history(main_window):
    history_dialog = QDialog(main_window)
    history_dialog.setWindowTitle(main_window.translate('History'))
    history_dialog.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
    history_dialog.setMinimumWidth(300)
    history_dialog.setMinimumHeight(300)

    layout = QVBoxLayout()

    history_list = QListWidget()
    history_data = load_history()
    for entry in history_data:
        item_text = f"{entry['timestamp']} - {entry['url']} (Search)" if entry.get('search') else f"{entry['timestamp']} - {entry['url']}"
        history_list.addItem(item_text)
        
    button_layout = QHBoxLayout()
    clear_button = QPushButton(main_window.translate('Clear history'))
    clear_button.clicked.connect(lambda: open_clear_history_dialog(main_window))
    button_layout.addWidget(clear_button)
    export_button = QPushButton(main_window.translate('Export'))
    export_button.clicked.connect(lambda: open_export_history_dialog(main_window))
    button_layout.addWidget(export_button)
    layout.addLayout(button_layout)
    
    layout.addWidget(history_list)
    history_dialog.setLayout(layout)
    history_dialog.exec_()
