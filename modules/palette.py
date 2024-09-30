from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def update_palette(self):
    palette = QPalette()
    if self.current_palette == 'dark':
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        # Set other dark mode colors
    else:
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        # Set other light mode colors
    self.setPalette(palette)

def toggle_palette(self):
    self.current_palette = 'light' if self.current_palette == 'dark' else 'dark'
    self.update_palette()
    self.save_settings()
    self.open_settings()
