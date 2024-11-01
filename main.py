import sys
from PySide6.QtWidgets import QApplication
from ui.mainWindow import PostureWatcherUI

def main():
    app = QApplication(sys.argv)
    mainWin = PostureWatcherUI()
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

