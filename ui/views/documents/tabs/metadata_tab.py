from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
)


class MetadataTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)