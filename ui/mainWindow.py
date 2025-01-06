import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QListWidget, QStackedWidget
from ui.dashboard import Dashboard
from ui.settings import Settings
from ui.home import CameraViewTab

class PostureWatcherUI(QWidget):
    def __init__(self):
        super().__init__()

        # Setup UI components
        self.init_ui()

    def init_ui(self):
        # Sidebar with navigation
        self.sidebar = QListWidget(self)
        self.sidebar.setFixedWidth(100)
        self.sidebar.addItem("Camera View")
        self.sidebar.addItem("Dashboard")
        self.sidebar.addItem("Settings")
        self.sidebar.currentRowChanged.connect(self.display_tab)

        # Create QStackedWidget to hold different tab views
        self.stacked_widget = QStackedWidget(self)

        # Create tabs
        self.camera_view_tab = CameraViewTab()
        self.dashboard_tab = Dashboard()
        self.settings_tab = Settings()

        # Add tabs to stacked widget
        self.stacked_widget.addWidget(self.camera_view_tab)
        self.stacked_widget.addWidget(self.dashboard_tab)
        self.stacked_widget.addWidget(self.settings_tab)

        # Layout for the main window
        layout = QHBoxLayout(self)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)
        self.setWindowTitle("Posture Watcher")
        self.resize(1024, 768)

    def display_tab(self, index):
        # Change the displayed tab when the user clicks a different item in the sidebar
        self.stacked_widget.setCurrentIndex(index)

def main():
    app = QApplication(sys.argv)
    mainWin = PostureWatcherUI()
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
