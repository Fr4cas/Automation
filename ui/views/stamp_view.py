from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
)


class StampView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        title = QLabel("Stamp")
        title.setObjectName("pageTitle")

        subtitle = QLabel("Stamp documents digitally.")
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()