from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QBrush


class ToggleSwitch(QPushButton):
    def __init__(self, parent=None, width=60, height=30, on_color="#4CAF50", off_color="#CCCCCC", circle_color="#FFFFFF"):
        """
        Reusable ToggleSwitch widget.

        :param parent: Parent widget.
        :param width: Width of the toggle switch.
        :param height: Height of the toggle switch.
        :param on_color: Background color when toggled on.
        :param off_color: Background color when toggled off.
        :param circle_color: Color of the toggle button.
        """
        super().__init__(parent)
        self.setCheckable(True)
        self.setChecked(False)
        self.setFixedSize(width, height)
        
        # Store customization parameters
        self.on_color = QColor(on_color)
        self.off_color = QColor(off_color)
        self.circle_color = QColor(circle_color)

        self.update_style()
        self.toggled.connect(self.update_style)

    def update_style(self):
        """Update the style of the toggle switch based on its state."""
        if self.isChecked():
            self.bg_color = self.on_color
            self.circle_x = self.width() - self.height() + 2
        else:
            self.bg_color = self.off_color
            self.circle_x = 2
        self.update()

    def paintEvent(self, event):
        """Custom paint event for rendering the toggle switch."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        brush = QBrush(self.bg_color)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() // 2, self.height() // 2)

        # Draw toggle
        brush = QBrush(self.circle_color)
        painter.setBrush(brush)
        painter.drawEllipse(self.circle_x, 2, self.height() - 4, self.height() - 4)

        painter.end()

