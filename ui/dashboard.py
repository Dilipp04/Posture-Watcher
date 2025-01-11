from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QProgressBar
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()
        self.bg_color = "#e0f7fa"
        self.text_color = "#000000"
        self.setWindowTitle("Dashboard")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(f"background-color:white;color:{self.text_color};")

        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        title = QLabel("DashBoard")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("margin:10px 10px; padding: 10px;")
        title.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title)

        # Header Section
        header = QWidget()
        header.setStyleSheet("background-color: #e0f7fa; border-radius: 10px; padding: 20px;")
        header_layout = QHBoxLayout(header)

        header_label = QLabel("Hii Good Morning")
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        header_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        header_image = QLabel()
        header_image.setPixmap(QPixmap("assets/dashboard_header.png").scaled(220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_image.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(header_image)
        main_layout.addWidget(header)

        # Statistics Row
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(self.create_stat_card("Today's", 72, "Success", self.bg_color))
        stats_layout.addWidget(self.create_stat_card("Total", 45, "Success", self.bg_color))
        stats_layout.addWidget(self.create_stat_card("Achievement", 72, "Goal", self.bg_color))

        main_layout.addLayout(stats_layout)

        # Progress and Usage Row
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)

        bottom_layout.addWidget(self.create_progress_card("Progress this Week", self.bg_color))
        bottom_layout.addWidget(self.create_progress_card("Usage this Week", self.bg_color))

        main_layout.addLayout(bottom_layout)

    def create_stat_card(self, title, value, subtitle, bg_color):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"background-color: {bg_color}; border-radius: 10px;padding: 10px;")
        layout = QHBoxLayout(card)  # Use horizontal layout to align text and chart
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Left Side: Title, Value, and Subtitle
        text_layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft)

        value_label = QLabel(f"{value}%")
        value_label.setFont(QFont("Arial", 28, QFont.Bold))
        value_label.setAlignment(Qt.AlignLeft)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Arial", 10))
        subtitle_label.setAlignment(Qt.AlignLeft)

        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        text_layout.addWidget(subtitle_label)

        # Right Side: Donut Chart
        donut_chart = self.create_donut_chart(value)

        layout.addLayout(text_layout)
        layout.addWidget(donut_chart, alignment=Qt.AlignRight)

        return card

    def create_donut_chart(self, percentage):
        # Create a Matplotlib figure for the donut chart
        fig, ax = plt.subplots(figsize=(2.5, 2.5))  # Adjust the figure size as needed
        fig.patch.set_alpha(0)  # Remove the background of the figure

        sizes = [percentage, 100 - percentage]
        colors = ['#00767C', '#e0e0e0']  # Colors for the segments

        ax.pie(
            sizes,
            colors=colors,
            startangle=90,
            wedgeprops={'width': 0.3, 'edgecolor': 'white'},  # 'width' makes it hollow
        )

        # Equal aspect ratio ensures the pie chart is drawn as a circle
        ax.axis('equal')
        ax.set_facecolor((1, 1, 1, 0))  # Set the axis background to transparent

        # Embed the chart into the PySide6 application using FigureCanvas
        canvas = FigureCanvas(fig)
        plt.close(fig)  # Close the figure to prevent it from showing separately

        return canvas

    def create_progress_card(self, title, bg_color):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"background-color: {bg_color}; border-radius: 10px;")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft)

        progress_layout = QVBoxLayout()
        for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
            # Create a horizontal layout for each day
            day_layout = QHBoxLayout()

            # Add a day label
            day_label = QLabel(f"{i+1} {day}")
            day_label.setFont(QFont("Arial", 10))
            day_label.setAlignment(Qt.AlignLeft)

            progress_prct_label = QLabel(f" 50%")
            progress_prct_label.setFont(QFont("Arial", 10))
            progress_prct_label.setAlignment(Qt.AlignRight)

            # Add a progress bar
            progress_bar = QProgressBar()
            progress_bar.setAlignment(Qt.AlignRight)
            progress_bar.setValue(50)  # Simulate 50% progress
            progress_bar.setFixedHeight(6)  # Adjust the height of the progress bar
            progress_bar.setTextVisible(False)  # Hide the percentage text
            progress_bar.setStyleSheet(
                """
                QProgressBar {
                    font-size: 4px;
                    border-radius: 5px;
                    background-color: white;
                }
                QProgressBar::chunk {
                    background-color: #00767C;
                    border-radius: 5px;
                }
                """
            )

            # Add widgets to the horizontal layout
            day_layout.addWidget(day_label, 1)  # Day label takes less space
            day_layout.addWidget(progress_prct_label, 1)  # Day label takes less space
            day_layout.addWidget(progress_bar, 10)  # Progress bar takes more space

            # Add the horizontal layout to the main progress layout
            progress_layout.addLayout(day_layout)

        layout.addWidget(title_label)
        layout.addLayout(progress_layout)

        return card


def main():
    import sys
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())


if __name__ == "_main_":
    main()