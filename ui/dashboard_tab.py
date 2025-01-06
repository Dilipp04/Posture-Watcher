from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame, QHBoxLayout , QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
class DashboardTab(QFrame):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout(self)

        # Greeting Card
        greeting_card = self.create_card("Welcome Back!", "Hope you’re having a good posture day!")
        layout.addWidget(greeting_card)

        # Rank and Today's Stats (Horizontal Layout)
        stats_layout = QHBoxLayout()

        rank_card = self.create_card("Rank", "Top 5% in PostureWatchers")
        stats_layout.addWidget(rank_card)

        today_stats_card = self.create_card("Today's Stats", "Good Posture: 80%\nBad Posture: 20%")
        stats_layout.addWidget(today_stats_card)

        layout.addLayout(stats_layout)

        # Monitoring and Weekly Good Posture Progress (Horizontal Layout)
        monitoring_layout = QHBoxLayout()

        monitoring_card = self.create_card("Monitoring", "Posture monitoring is ON")
        monitoring_layout.addWidget(monitoring_card)

        weekly_good_posture_card = self.create_progress_card("Weekly Good Posture Progress", 70)
        monitoring_layout.addWidget(weekly_good_posture_card)

        layout.addLayout(monitoring_layout)

        # App Usage Progress Card
        usage_card = self.create_progress_card("App Usage", 2, "2 hours today")
        layout.addWidget(usage_card)

    def create_card(self, title: str, content: str) -> QFrame:
        """Creates a styled card with title and content."""
        card = QFrame()
        card.setFrameShape(QFrame.Box)
        card.setLineWidth(2)
        card_layout = QVBoxLayout(card)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)

        # Content
        content_label = QLabel(content)
        content_label.setFont(QFont("Arial", 12))
        content_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(content_label)

        return card

    def create_progress_card(self, title: str, progress: int, extra_text: str = "") -> QFrame:
        """Creates a card with a progress bar."""
        card = QFrame()
        card.setFrameShape(QFrame.Box)
        card.setLineWidth(2)
        card_layout = QVBoxLayout(card)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)

        # Progress Bar
        progress_bar = QProgressBar()
        progress_bar.setValue(progress)
        card_layout.addWidget(progress_bar)

        # Extra text below the progress bar
        if extra_text:
            extra_label = QLabel(extra_text)
            extra_label.setFont(QFont("Arial", 12))
            extra_label.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(extra_label)

        return card

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardTab()
    window.show()
    sys.exit(app.exec())
