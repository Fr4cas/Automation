from ui.widgets.metric_card import MetricCard
from ui.widgets.dashboard_panel import DashboardPanel

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame,
    )


class OverviewView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        title = QLabel("Welcome back!")
        title.setObjectName("pageTitle")

        subtitle = QLabel("Here's your overview")
        subtitle.setObjectName("pageSubtitle")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        self.start_button = QPushButton("Start Processing")
        self.start_button.setObjectName("startButton")

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.start_button)

        layout.addLayout(header_layout)

        # KPI Cards
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(16)

        self.scanned_card = MetricCard("Scanned", "0")
        self.successful_card = MetricCard("Successful", "0")
        self.failed_card = MetricCard("Failed", "0")
        self.duration_card = MetricCard("Duration", "0s")

        metrics_layout.addWidget(self.scanned_card, 1)
        metrics_layout.addWidget(self.successful_card, 1)
        metrics_layout.addWidget(self.failed_card, 1)
        metrics_layout.addWidget(self.duration_card, 1)

        layout.addLayout(metrics_layout)

        # Dashboard Panels
        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(16)

        self.processing_panel = DashboardPanel("Processing Overview")
        self.activity_panel = DashboardPanel("Recent Activity")

        panels_layout.addWidget(self.processing_panel)
        panels_layout.addWidget(self.activity_panel)

        layout.addLayout(panels_layout)