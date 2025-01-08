import sys
from ui.home import Home
from ui.settings import Settings
from ui.dashboard import Dashboard
from ui.mainWindow import PostureWatcherUI
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Home()
    window.showMaximized()
    sys.exit(app.exec())
