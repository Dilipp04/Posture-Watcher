from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, Qt

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Settings tab layout
        layout = QVBoxLayout(self)

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        setting_label = QLabel("Adjust Sensitivity (placeholder)")
        layout.addWidget(setting_label)
