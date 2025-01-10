import sys
from ui.home import Home
from ui.settings import Settings
from ui.dashboard import Dashboard
from ui.mainWindow import PostureWatcherUI
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

def main():

    app = QApplication(sys.argv)
    window = PostureWatcherUI()
    window.showMaximized()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
