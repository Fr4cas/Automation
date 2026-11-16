from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
)


class DocumentsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        title = QLabel("Processed Documents")
        title.setObjectName("pageTitle")

        subtitle = QLabel("Review your processed documents.")
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()