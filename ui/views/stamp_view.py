from PySide6.QtCore import QDate, Qt

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QDateEdit,
    QPushButton, QFrame, QSizePolicy,
)


class StampView(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("stampPage")

        # Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Header
        title = QLabel("Stamp")
        title.setObjectName("pageTitle")

        subtitle = QLabel("Configure and apply document stamps.")
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # =====================================
        # TOP SECTION
        # =====================================

        top_layout = QHBoxLayout()
        top_layout.setSpacing(12)

        # Document Number Card
        number_section = QFrame()
        number_section.setObjectName("stampCard")

        number_layout = QVBoxLayout(number_section)
        number_layout.setContentsMargins(12, 12, 12, 12)
        number_layout.setSpacing(6)

        number_header = self.create_section_header(
            "Document Number",
            "Set the starting document number."
        )
        number_layout.addWidget(number_header)

        number_layout.addWidget(QLabel("Starting Number"))

        self.start_number = QSpinBox()
        self.start_number.setRange(1, 999)
        self.start_number.setValue(1)

        number_layout.addWidget(self.start_number)

        # Received Stamp Card
        date_section = QFrame()
        date_section.setObjectName("stampCard")

        date_layout = QVBoxLayout(date_section)
        date_layout.setContentsMargins(12, 12, 12, 12)
        date_layout.setSpacing(6)

        date_header = self.create_section_header(
            "Received Stamp",
            "Choose the date shown on the stamp."
        )
        date_layout.addWidget(date_header)

        date_layout.addWidget(QLabel("Received Date"))

        self.received_date = QDateEdit()
        self.received_date.setCalendarPopup(True)
        self.received_date.setDate(QDate.currentDate())
        self.received_date.setDisplayFormat("yyyy/MM/dd")

        date_layout.addWidget(self.received_date)

        top_layout.addWidget(number_section, 1)
        top_layout.addWidget(date_section, 1)

        layout.addLayout(top_layout)

        # =====================================
        # MIDDLE SECTION
        # =====================================

        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(12)

        # Stamp Positions Card
        position_section = QFrame()
        position_section.setObjectName("stampCard")

        position_layout = QVBoxLayout(position_section)
        position_layout.setContentsMargins(12, 12, 12, 12)
        position_layout.setSpacing(12)

        position_header = self.create_section_header(
            "Stamp Positions",
            "Set where stamps appear on the document."
        )
        position_layout.addWidget(position_header)

        # Document Number Position
        number_position = QHBoxLayout()
        number_position.setSpacing(8)

        number_info = QVBoxLayout()
        number_info.setSpacing(2)

        number_label = QLabel("Document Number")
        number_label.setObjectName("positionName")

        number_description = QLabel("Current position")
        number_description.setObjectName("positionDescription")

        number_info.addWidget(number_label)
        number_info.addWidget(number_description)

        self.number_position_label = QLabel("First Page · Top")
        self.number_position_label.setObjectName("positionValue")

        self.number_change_button = QPushButton("Change Position")
        self.number_change_button.setObjectName("numberChangeButton")

        number_position.addLayout(number_info)
        number_position.addStretch()
        number_position.addWidget(self.number_position_label)
        number_position.addWidget(self.number_change_button)

        # Received Stamp Position
        received_position = QHBoxLayout()
        received_position.setSpacing(8)

        received_info = QVBoxLayout()
        received_info.setSpacing(2)

        received_label = QLabel("Received Stamp")
        received_label.setObjectName("positionName")

        received_description = QLabel("Current position")
        received_description.setObjectName("positionDescription")

        received_info.addWidget(received_label)
        received_info.addWidget(received_description)

        self.received_position_label = QLabel("Last Page · Bottom")
        self.received_position_label.setObjectName("positionValue")

        self.received_change_button = QPushButton("Change Position")
        self.received_change_button.setObjectName("receivedChangeButton")

        received_position.addLayout(received_info)
        received_position.addStretch()
        received_position.addWidget(self.received_position_label)
        received_position.addWidget(self.received_change_button)

        position_layout.addLayout(number_position)
        position_layout.addLayout(received_position)

        # Position Preview Card
        preview_section = QFrame()
        preview_section.setObjectName("stampCard")

        preview_layout = QVBoxLayout(preview_section)
        preview_layout.setContentsMargins(12, 12, 12, 12)
        preview_layout.setSpacing(8)

        preview_title = QLabel("Position Preview")
        preview_title.setObjectName("panelTitle")

        preview_layout.addWidget(preview_title)

        # Miniature document
        self.position_preview = QFrame()
        self.position_preview.setObjectName("previewPaper")
        self.position_preview.setMinimumHeight(145)
        self.position_preview.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        paper_layout = QVBoxLayout(self.position_preview)
        paper_layout.setContentsMargins(12, 8, 12, 8)
        paper_layout.setSpacing(5)

        self.preview_number = QLabel()
        self.preview_number.setObjectName("previewNumber")
        self.preview_number.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        paper_layout.addWidget(self.preview_number)

        # Simulated document lines
        for width in (90, 75, 85, 65, 80, 55):
            line = QFrame()
            line.setObjectName("previewLine")
            line.setFixedSize(width, 3)
            paper_layout.addWidget(line)

        paper_layout.addStretch()

        self.preview_received = QLabel()
        self.preview_received.setObjectName("previewReceived")
        self.preview_received.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        paper_layout.addWidget(
            self.preview_received,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        preview_layout.addWidget(self.position_preview)

        middle_layout.addWidget(position_section, 3)
        middle_layout.addWidget(preview_section, 2)

        layout.addLayout(middle_layout)

        # =====================================
        # PROCESSING SECTION
        # =====================================

        processing_section = QFrame()
        processing_section.setObjectName("stampCard")

        processing_layout = QVBoxLayout(processing_section)
        processing_layout.setContentsMargins(12, 10, 12, 10)
        processing_layout.setSpacing(8)

        processing_header = self.create_section_header(
            "Processing",
            "Apply stamps to selected documents."
        )

        processing_layout.addWidget(processing_header)

        self.status_label = QLabel("Ready to stamp documents.")
        self.status_label.setObjectName("statusLabel")

        processing_layout.addWidget(self.status_label)

        self.start_button = QPushButton("Start Stamping")
        self.start_button.setObjectName("primaryButton")
        self.start_button.setMinimumHeight(36)

        processing_layout.addWidget(self.start_button)

        layout.addWidget(processing_section)
        layout.addStretch()

        # =====================================
        # PREVIEW CONNECTIONS
        # =====================================

        self.start_number.valueChanged.connect(
            self.update_position_preview
        )

        self.received_date.dateChanged.connect(
            self.update_position_preview
        )

        self.update_position_preview()

    # =====================================
    # SECTION HEADER
    # =====================================

    def create_section_header(self, title_text, description_text):
        container = QWidget()

        header_layout = QVBoxLayout(container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)

        title = QLabel(title_text)
        title.setObjectName("panelTitle")

        description = QLabel(description_text)
        description.setObjectName("sectionDescription")

        header_layout.addWidget(title)
        header_layout.addWidget(description)

        return container

    # =====================================
    # PREVIEW UPDATE
    # =====================================

    def update_position_preview(self):
        number = self.start_number.value()

        received_date = self.received_date.date().toString(
            "yyyy/MM/dd"
        )

        self.preview_number.setText(f"No. {number:03d}")

        self.preview_received.setText(
            f"收 文\n{received_date}"
        )

    # =====================================
    # STAMP SETTINGS
    # =====================================

    def get_stamp_settings(self):
        return {
            "start_number": self.start_number.value(),
            "received_date": self.received_date.date().toPython(),
        }

    def set_status(self, message):
        self.status_label.setText(message)
