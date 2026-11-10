from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel,
)

class MetricCard(QFrame):
    def __init__(self, title, value):
        super().__init__()

        self.setObjectName("metricCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        self.title_label = QLabel(title)
        self.value_label = QLabel(value)

        self.title_label.setObjectName("metricTitle")
        self.value_label.setObjectName("metricValue")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value):
        self.value_label.setText(str(value))