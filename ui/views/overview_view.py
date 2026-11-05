from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,
    )


class OverviewView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        title = QLabel("Welcome back!")
        subtitle = QLabel("Here's your overview")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        self.start_button = QPushButton("Start Processing")
        self.start_button.setObjectName("startButton")
        self.start_button.setEnabled(False)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.start_button)

        layout.addLayout(header_layout)
