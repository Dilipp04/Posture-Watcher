from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox,
    QHBoxLayout, QPushButton, QButtonGroup, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from utilities.state import State

class Settings(QWidget):
    def __init__(self,state:State):
        super().__init__()

        self.state = state
        self.setStyleSheet("background-color:white;color:black;padding:10px")
        main_layout = QVBoxLayout(self)

        # Settings Title
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("margin:10px 10px; padding: 10px;color:#013e54;")
        main_layout.addWidget(title, alignment=Qt.AlignLeft)

        # Create QListWidget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("QListWidget { border: none; }")
        self.list_widget.setSpacing(10)
        main_layout.addWidget(self.list_widget)

        # Add sections to the QListWidget
        self.add_section(
            "Camera",
            "Choose your preferred webcam from the list",
            self.create_camera_dropdown()
        )
        self.add_section(
            "Camera Angle",
            "",
            self.create_toggle_buttons(["Front", "Side"], "camera_angle")
        )
        self.add_section(
            "Position",
            "",
            self.create_toggle_buttons(["Left", "Center", "Right"],"position")
        )
        self.add_section(
            "Delay",
            "",
            self.create_toggle_buttons(["3", "10", "15"], "delay")
        )

    def add_section(self, title, description, widget):
        """Add a section as a QListWidgetItem with a custom widget."""
        # Create the main container widget
        container = QWidget()
        container.setStyleSheet("background-color: white; padding: 20px 0px;")

        # Create a horizontal layout for the section
        layout = QHBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a vertical layout for the title and description
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        text_layout.setContentsMargins(0, 0, 0, 0)

        # Add title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14))
        text_layout.addWidget(title_label)

        # Add description (if provided)
        if description:
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Arial", 10))
            desc_label.setStyleSheet("color: gray;")
            desc_label.setWordWrap(True)
            text_layout.addWidget(desc_label)

        # Add layouts to the horizontal layout
        layout.addLayout(text_layout)  # Add text layout on the left
        layout.addWidget(widget, alignment=Qt.AlignRight)  # Add the widget on the right

        # Create QListWidgetItem
        item = QListWidgetItem()
        item.setSizeHint(container.sizeHint())  # Match the size of the widget
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, container)

    def create_camera_dropdown(self):
        """Create a dropdown menu for camera selection."""
        dropdown = QComboBox()
        dropdown.addItems(["Webcam", "Virtual Camera", "External Camera"])
        dropdown.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
                color: #333;
            }
            QComboBox:hover {
                border: 1px solid #4CAF50;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url('assets/dropdown_arrow.svg');
                width: 20px;
                height: 20px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
                color: #333;
                selection-background-color: #4CAF50;
                selection-color: white;
            }
        """)

        dropdown.setFixedSize(230, 30)

        # Connect to state update
        dropdown.currentTextChanged.connect(
            lambda value: self.state.update_setting("camera", dropdown.currentIndex())
        )
        return dropdown

    def create_toggle_buttons(self, options, state_key):
        """Create a row of toggle buttons."""
        container = QWidget()
        container.setFixedSize(230, 40)
        container.setStyleSheet("""
            QWidget {
                border: none;
                background-color: #023D53;
                border-radius: 10px;
            }
        """)
        layout = QHBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)

        button_group = QButtonGroup(container)
        for option in options:
            button = QPushButton(option)
            button.setCheckable(True)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 15px;
                    background-color: #023D53;
                    color: white;
                }
                QPushButton:checked {
                    background-color: white;
                    color: #023D53;
                    border: none;
                }
            """)
            layout.addWidget(button)
            button_group.addButton(button)

            # Connect each button to update state
            button.clicked.connect(
                lambda checked, value=option: self.state.update_setting(state_key, value) if checked else None
            )

        # Set the first button as checked by default
        if button_group.buttons():
            button_group.buttons()[0].setChecked(True)
            self.state.update_setting(state_key, options[0])

        return container