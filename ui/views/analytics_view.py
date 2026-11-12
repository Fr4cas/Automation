from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
)


class AnalyticsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        title = QLabel("Analytics")
        title.setObjectName("pageTitle")

        subtitle = QLabel("View processing statistics and performance.")
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
