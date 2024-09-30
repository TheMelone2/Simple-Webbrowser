import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .translation import change_language

def change_search_engine(main_window):
    main_window.selected_search_engine = main_window.search_engine_combobox.currentText()
    main_window.start_url = main_window.SEARCH_ENGINES[main_window.selected_search_engine]
    set_search_engine(main_window, main_window.start_url)
    save_settings(main_window)
    update_search_engine_menu(main_window)

def set_search_engine(main_window, url):
    main_window.selected_search_engine = [key for key, value in main_window.SEARCH_ENGINES.items() if value == url][0]
    main_window.start_url = url
    save_settings(main_window)
    main_window.current_browser().setUrl(QUrl(main_window.start_url))
    update_search_engine_menu(main_window)

def load_settings(main_window):
    try:
        with open('settings.json', 'r') as file:
            settings = json.load(file)
            main_window.bookmarks = settings.get('bookmarks', [])
            main_window.current_palette = settings.get('palette', 'dark')
            main_window.selected_search_engine = settings.get('search_engine', 'Ecosia')
            main_window.start_url = main_window.SEARCH_ENGINES[main_window.selected_search_engine]
            main_window.current_language = settings.get('language', 'en')
    except FileNotFoundError:
        main_window.bookmarks = []
        main_window.current_palette = 'dark'
        main_window.selected_search_engine = 'Ecosia'
        main_window.start_url = main_window.SEARCH_ENGINES[main_window.selected_search_engine]
        main_window.current_language = 'en'

def save_settings(main_window):
    settings = {
        'bookmarks': main_window.bookmarks,
        'palette': main_window.current_palette,
        'search_engine': main_window.selected_search_engine,
        'language': main_window.current_language
    }
    with open('settings.json', 'w') as file:
        json.dump(settings, file, indent=4)

def toggle_palette(main_window):
    if main_window.current_palette == 'dark':
        main_window.current_palette = 'light'
    else:
        main_window.current_palette = 'dark'
    save_settings(main_window)
    update_palette(main_window)

def update_palette(main_window):
    if main_window.current_palette == 'dark':
        QApplication.setStyle("Fusion")
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(dark_palette)
    else:
        QApplication.setPalette(QApplication.style().standardPalette())

def open_settings(main_window):
    settings_dialog = QDialog(main_window)
    settings_dialog.setWindowTitle(main_window.translate('Settings'))
    settings_dialog.setFixedSize(500, 400)

    layout = QVBoxLayout()

    search_engine_label = QLabel(main_window.translate('Search Engine') + ':')
    layout.addWidget(search_engine_label)

    main_window.search_engine_combobox = QComboBox()
    for engine in main_window.SEARCH_ENGINES:
        main_window.search_engine_combobox.addItem(engine)
    main_window.search_engine_combobox.setCurrentText(main_window.selected_search_engine)
    main_window.search_engine_combobox.currentIndexChanged.connect(lambda: change_search_engine(main_window))
    layout.addWidget(main_window.search_engine_combobox)

    mode_toggle = QPushButton(main_window.translate('Light Mode') if main_window.current_palette == 'dark' else main_window.translate('Dark Mode'))
    mode_toggle.clicked.connect(main_window.toggle_palette)
    layout.addWidget(mode_toggle)

    bookmark_layout = QVBoxLayout()
    bookmark_layout.addWidget(QLabel(main_window.translate('Bookmarks') + ':'))

    main_window.bookmark_list = QListWidget()
    for bookmark in main_window.bookmarks:
        main_window.bookmark_list.addItem(bookmark)
    bookmark_layout.addWidget(main_window.bookmark_list)

    add_bookmark_btn = QPushButton(main_window.translate('Add Bookmark'))
    add_bookmark_btn.clicked.connect(main_window.add_bookmark)
    bookmark_layout.addWidget(add_bookmark_btn)

    remove_bookmark_btn = QPushButton(main_window.translate('Remove Bookmark'))
    remove_bookmark_btn.clicked.connect(main_window.remove_bookmark)
    bookmark_layout.addWidget(remove_bookmark_btn)

    layout.addLayout(bookmark_layout)

    language_label = QLabel(main_window.translate('Language') + ':')
    layout.addWidget(language_label)

    main_window.language_combobox = QComboBox()
    for lang in ['en', 'de']:  # Add more languages if needed
        main_window.language_combobox.addItem(lang)
    main_window.language_combobox.setCurrentText(main_window.current_language)
    main_window.language_combobox.currentIndexChanged.connect(main_window.change_language)
    layout.addWidget(main_window.language_combobox)

    shortcuts_label = QLabel(main_window.translate('Shortcuts') + ':')
    layout.addWidget(shortcuts_label)
    shortcuts_text = QTextEdit()
    shortcuts_text.setReadOnly(True)
    shortcuts_text.setPlainText(main_window.translate('New Tab') + ': Ctrl + N\n' +
                                main_window.translate('History') + ': Ctrl + H\n' +
                                main_window.translate('Settings') + ': Ctrl + E\n' +
                                main_window.translate('Add Bookmark') + ': Ctrl + B')
    layout.addWidget(shortcuts_text)
    
    credits_button = QPushButton(main_window.translate('Credits'))
    credits_button.clicked.connect(main_window.open_credits)
    layout.addWidget(credits_button)
    

    settings_dialog.setLayout(layout)
    settings_dialog.exec_()
    

def open_credits(main_window):
    credits_dialog = QDialog(main_window)
    credits_dialog.setWindowTitle(main_window.translate('Credits'))
    credits_dialog.setFixedSize(300, 200)
    
    layout = QVBoxLayout()
    credits_label = QLabel(main_window.translate('Credits') + ':')
    layout.addWidget(credits_label)

def update_search_engine_menu(main_window):
    main_window.search_engine_menu.clear()
    for engine, url in main_window.SEARCH_ENGINES.items():
        action = QAction(engine, main_window)
        action.setCheckable(True)
        action.setChecked(url == main_window.start_url)
        action.triggered.connect(lambda _, url=url: set_search_engine(main_window, url))
        main_window.search_engine_menu.addAction(action)
    