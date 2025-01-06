from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel ,QFrame
from PySide6.QtCore import QTimer, Qt

class SettingsTab(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        
        # Settings tab layout
        layout = QVBoxLayout(self)

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        label = QLabel("Settings Page")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #333;")
        
        layout.addWidget(label)

