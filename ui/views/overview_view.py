from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class OverviewView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Welcome back!")
        layout.addWidget(title)
