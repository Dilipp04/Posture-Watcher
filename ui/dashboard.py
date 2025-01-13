from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QProgressBar
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import csv

class Dashboard(QWidget):

    def __init__(self):
        super().__init__()
        self.bg_color = "#e0f7fa"
        self.text_color = "#013e54"
        self.setWindowTitle("Dashboard")
        self.setStyleSheet(f"background-color:white;color:{self.text_color};")
        self.data_file = "history.csv"
        self.data = self.load_data()
        self.setup_ui()

    def load_data(self):
        """Load data from the given CSV file."""
        data = []
        try:
            with open(self.data_file, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append({
                        "date": row["Date"],
                        "total_minutes": float(row["Total Minutes"]),
                        "good_posture_minutes": float(row["Good Posture Minutes"]),
                    })
        except FileNotFoundError:
            print(f"File {self.data_file} not found.")
        return data[-7:]  # Return only the last 7 days

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
        header.setStyleSheet("background-color: #e0f7fa; border-radius: 10px; padding: 5px;")
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

        stats_layout.addWidget(self.create_stat_card("Today's", self.get_today(), "Success", self.bg_color))
        stats_layout.addWidget(self.create_stat_card("Total", self.get_total(), "Success", self.bg_color))
        stats_layout.addWidget(self.create_Achivement_card("Achievement",  "Goal", self.bg_color))

        main_layout.addLayout(stats_layout)

        # Progress and Usage Row
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)

        bottom_layout.addWidget(self.create_progress_card("Progress this Week",self.data, self.bg_color))
        bottom_layout.addWidget(self.create_progress_card("Usage this Week",self.data, self.bg_color))

        main_layout.addLayout(bottom_layout)

    

    def create_stat_card(self, title, value,subtitle, bg_color):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"background-color: {bg_color}; border-radius: 10px;padding: 3px;")
        layout = QHBoxLayout(card)  # Use horizontal layout to align text and chart
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Left Side: Title, Value, and Subtitle
        text_layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft)

        value_label = QLabel(f"{value}")
        value_label.setFont(QFont("Arial", 25, QFont.Bold))
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

    def create_Achivement_card(self, title, subtitle, bg_color):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"background-color: {bg_color}; border-radius: 10px;padding: 3px;")
        layout = QHBoxLayout(card)  # Use horizontal layout to align text and chart
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Left Side: Title, Value, and Subtitle
        text_layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft)

        result = self.get_total()
        if result>80 :
            value= "Excellent"
        elif result>70 :
            value="Good"
        elif result>50 :
            value="Average"
        else :
            value="Poor"

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 25, QFont.Bold))
        value_label.setAlignment(Qt.AlignLeft)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Arial", 10))
        subtitle_label.setAlignment(Qt.AlignLeft)

        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        text_layout.addWidget(subtitle_label)

        layout.addLayout(text_layout)

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

    def create_progress_card(self, title, weekly_data, bg_color):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"background-color: {bg_color}; border-radius: 10px; ")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft)

        progress_layout = QVBoxLayout()
        for day_data in weekly_data:
            day_layout = QHBoxLayout()

            day_label = QLabel(f"{day_data["date"].split(" ")[0]} {day_data["date"].split(" ")[1]}")  # Use data value
            day_label.setFont(QFont("Arial", 10))
            day_label.setAlignment(Qt.AlignLeft)

            percentage = self.get_percentage(day_data["good_posture_minutes"], day_data["total_minutes"])

            percent_label = QLabel(f"{percentage}%")  # Use data value
            percent_label.setFont(QFont("Arial", 10))
            percent_label.setAlignment(Qt.AlignLeft)

            progress_bar = QProgressBar()
            progress_bar.setAlignment(Qt.AlignRight)
            progress_bar.setValue(percentage)  # Use data value
            progress_bar.setFixedHeight(6)
            progress_bar.setTextVisible(False)
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

            day_layout.addWidget(day_label, 1)
            day_layout.addWidget(progress_bar, 10)
            day_layout.addWidget(percent_label, 1)
            progress_layout.addLayout(day_layout)

        layout.addWidget(title_label)
        layout.addLayout(progress_layout)

        return card

    def get_today(self):
        result = self.get_percentage(self.data[-1]["good_posture_minutes"],self.data[-1]["total_minutes"])
        return round(result,2)
    
    def get_total(self):
        sum_TM = 0
        sum_GM = 0
        for day in self.data:
            sum_TM += day["total_minutes"]
            sum_GM += day["good_posture_minutes"]
        result = self.get_percentage(sum_GM,sum_TM)
        return result
      
        
    @staticmethod
    def get_percentage(good_posture_minutes, total_minutes):
        result =  ( good_posture_minutes/ total_minutes * 100) if total_minutes > 0 else 0
        return round(result,2)

def main():
    import sys
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())


if __name__ == "_main_":
    main()