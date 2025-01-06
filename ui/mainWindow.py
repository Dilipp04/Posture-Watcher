import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout,QStackedWidget, QLabel, QProgressBar, QFrame, QHBoxLayout , QApplication ,QPushButton
from PySide6.QtCore import Qt 
from PySide6.QtGui import QFont ,QPixmap , QIcon
from ui.dashboard import Dashboard
from ui.settings import Settings
from ui.home import Home
class PostureWatcherUI(QWidget):
    def __init__(self):
        # Setup UI components
        self.init_ui()

    def init_ui(self):
        super().__init__()
        self.setWindowTitle("Posture Monitor")
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QHBoxLayout(self)
        self.setStyleSheet("background-color: #f3f4f6;")

        # Sidebar
        self.sidebar = self.sidebar()
        main_layout.addWidget(self.sidebar, 1)

        # Content area with stacked widget
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("background-color: white;")
        main_layout.addWidget(self.content_area, 10)

        # Create tabs
        self.camera_view_tab = Home()
        self.dashboard_tab = Dashboard()
        self.settings_tab = Settings()

        # Add tabs to stacked widget
        self.content_area.addWidget(self.camera_view_tab)
        self.content_area.addWidget(self.dashboard_tab)
        self.content_area.addWidget(self.settings_tab)
    
    def sidebar(self):
        # Sidebar container
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #013d54;border-radius: 10px;")
        sidebar_layout = QVBoxLayout(sidebar)

        # Logo
        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        logo.setPixmap(QPixmap("assets/logo-transparent1.png").scaled(100, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setStyleSheet("margin:20px 10px")
        sidebar_layout.addWidget(logo)

        # Navigation buttons
        nav_buttons = [
            ("Home", "assets/home_icon.svg"),
            ("Dashboard", "assets/dashboard_icon.svg"),
            ("Settings", "assets/settings_icon.svg")
        ]
        self.nav_button_dict = {}
        for text, icon_path in nav_buttons:
            button = QPushButton()
            button.setText(text)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QPixmap(icon_path).scaled(20, 20, Qt.KeepAspectRatio).size())
            button.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                    font-size: 16px;
                    text-align: left;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #005f73;
                }
                QPushButton:hover QIcon {
                    color: #000000; /* Change SVG icon color on hover */
                }
            """)
            sidebar_layout.addWidget(button)
            self.nav_button_dict[text] = button
        
        self.nav_button_dict["Home"].clicked.connect(lambda: self.content_area.setCurrentIndex(0))
        self.nav_button_dict["Dashboard"].clicked.connect(lambda: self.content_area.setCurrentIndex(1))
        self.nav_button_dict["Settings"].clicked.connect(lambda: self.content_area.setCurrentIndex(2))

        sidebar_layout.addStretch()
        return sidebar


def main():
    app = QApplication(sys.argv)
    mainWin = PostureWatcherUI()
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
