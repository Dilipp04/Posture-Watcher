from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QApplication
from PySide6.QtCore import Qt, QTimer, QPoint,QSize
from PySide6.QtGui import QFont, QIcon, QPixmap
import sys

class MiniWindow(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.init_ui()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.elapsed_time_timer = self.mainWindow.home.elapsed_time_timer
        self.elapsed_time_timer.timeout.connect(self.update_elapsed_time)
        self.is_dragging = False

    def init_ui(self):
        self.setFixedSize(230, 40)
        self.setStyleSheet("background-color:transparent;color:none")

        self.maximize_button = self.create_button("assets/maximize_button.svg")
        self.maximize_button.setIconSize(QSize(25, 25))
        self.maximize_button.clicked.connect(self.showMaximized)

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("assets/logo-transparent1.png").scaled(60, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.timer_label = QLabel("00:00", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 16))
        self.timer_label.setStyleSheet("color: white;")
        

        self.start_button = self.create_button("assets/play_icon.svg", checkable=True)
        self.start_button.toggled.connect(self.mainWindow.home.start_monitoring)
        self.pause_button = self.create_button("assets/pause_icon.svg", checkable=True)
        self.pause_button.toggled.connect(self.mainWindow.home.stop_monitoring)

        mainWidget = QWidget(self)
        mainWidget.setStyleSheet("background-color: #013e54;border-radius: 5px;")

        layout = QHBoxLayout(mainWidget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.logo)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)

    def create_button(self, icon_path, checkable=False):
        button = QPushButton(self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(20, 20))
        button.setFixedSize(28, 28)
        button.setStyleSheet("""
                QPushButton {   
                            background-color: transparent;
                            }
                QPushButton:hover {
                                background-color: #005f73;
                            }
                        """)
        button.setCheckable(checkable)
        return button
    
    def update_elapsed_time(self):
        minutes = self.mainWindow.home.elapsed_time // 60
        seconds = self.mainWindow.home.elapsed_time % 60
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_position)
            self.drag_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
    
    def showMaximized(self):
        self.mainWindow.show()
        self.hide()

def main():
    app = QApplication(sys.argv)
    mini_window = MiniWindow()
    mini_window.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
