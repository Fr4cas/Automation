from PySide6.QtCore import QDate

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QDateEdit,
    QPushButton, QFrame
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

        # Document Number Section
        number_section = QFrame()
        number_layout = QVBoxLayout(number_section)

        number_title = QLabel("Document Number")
        number_title.setObjectName("panelTitle")

        self.start_number = QSpinBox()
        self.start_number.setMinimum(1)
        self.start_number.setMaximum(999)
        self.start_number.setValue(1)

        number_layout.addWidget(number_title)
        number_layout.addWidget(QLabel("Starting Number"))
        number_layout.addWidget(self.start_number)

        layout.addWidget(number_section)

        # Received Stamp Section
        date_section = QFrame()
        date_layout = QVBoxLayout(date_section)

        date_title = QLabel("Received Stamp")
        date_title.setObjectName("panelTitle")

        self.received_date = QDateEdit()
        self.received_date.setCalendarPopup(True)
        self.received_date.setDate(QDate.currentDate())
        self.received_date.setDisplayFormat("yyyy/MM/dd")

        date_layout.addWidget(date_title)
        date_layout.addWidget(QLabel("Received Date"))
        date_layout.addWidget(self.received_date)

        layout.addWidget(date_section)

        # Stamp Position Section
        position_section = QFrame()
        position_layout = QVBoxLayout(position_section)

        position_title = QLabel("Stamp Positions")
        position_title.setObjectName("panelTitle")

        # Document Number Position
        number_position = QHBoxLayout()

        number_label = QLabel("Document Number")
        self.number_position_label = QLabel("First Page - Top")

        number_position.addWidget(number_label)
        number_position.addStretch()
        number_position.addWidget(self.number_position_label)

        # Received Stamp Position
        received_position = QHBoxLayout()

        received_label = QLabel("Received Stamp")
        self.received_position_label = QLabel("Last Page - Bottom")

        received_position.addWidget(received_label)
        received_position.addStretch()
        received_position.addWidget(self.received_position_label)

        position_layout.addWidget(position_title)
        position_layout.addLayout(number_position)
        position_layout.addLayout(received_position)

        layout.addWidget(position_section)

        # Processing Section
        processing_section = QFrame()
        processing_layout = QVBoxLayout(processing_section)

        processing_title = QLabel("Processing")
        processing_title.setObjectName("panelTitle")

        self.start_button = QPushButton("Start Stamping")

        self.status_label = QLabel("Ready to stamp documents.")
        self.status_label.setObjectName("pageSubtitle")

        processing_layout.addWidget(processing_title)
        processing_layout.addWidget(self.start_button)
        processing_layout.addWidget(self.status_label)

        layout.addWidget(processing_section)

        layout.addStretch()