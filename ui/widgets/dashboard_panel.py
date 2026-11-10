from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel,
)


class DashboardPanel(QFrame):
    def __init__(self, title):
        super().__init__()

        self.setObjectName("dashboardPanel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("panelTitle")

        layout.addWidget(self.title_label)

        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(8)

        layout.addLayout(self.content_layout)