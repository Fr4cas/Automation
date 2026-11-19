from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont, QFontMetrics, QResizeEvent

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QDateEdit, QDialog,
    QFormLayout, QDialogButtonBox, QPushButton,
    QFrame, QSizePolicy,
)


class PositionPreview(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("previewPaper")

        self.number_stamp = QLabel("2300A-YYMMDD-001", self)
        self.number_stamp.setObjectName("previewNumber")
        self.number_stamp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.received_stamp = QLabel("收 文\n2026/01/01", self)
        self.received_stamp.setObjectName("previewReceived")
        self.received_stamp.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.number_placement = {"x": 90, "y": 1, "scale": 80}
        self.received_placement = {"x": 90, "y": 95, "scale": 100}

    def set_placements(self, number_placement, received_placement):
        self.number_placement = number_placement
        self.received_placement = received_placement
        self.update_stamp_geometry()

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.update_stamp_geometry()

    def update_stamp_geometry(self):
        paper = self.rect().adjusted(10, 8, -10, -8)
        if paper.width() <= 0 or paper.height() <= 0:
            return

        self._place_stamp(
            self.number_stamp, self.number_placement,
            paper, 0.34, 18
        )
        self._fit_number_text()
        self._place_stamp(
            self.received_stamp, self.received_placement,
            paper, 0.48, 34
        )

    def _fit_number_text(self):
        font = self.number_stamp.font()
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 100)
        text_width = QFontMetrics(font).horizontalAdvance(
            self.number_stamp.text()
        )
        available_width = max(1, self.number_stamp.width() - 12)

        if text_width > available_width:
            font.setLetterSpacing(
                QFont.SpacingType.PercentageSpacing,
                max(1, int(available_width * 100 / text_width))
            )
        self.number_stamp.setFont(font)

    @staticmethod
    def _place_stamp(label, placement, paper, base_width_ratio, base_height):
        scale = placement["scale"] / 100
        width = min(
            paper.width(),
            max(1, round(paper.width() * base_width_ratio * scale))
        )
        height = min(paper.height(), max(1, round(base_height * scale)))
        x = paper.x() + round(
            max(0, paper.width() - width) * placement["x"] / 100
        )
        y = paper.y() + round(
            max(0, paper.height() - height) * placement["y"] / 100
        )
        label.setGeometry(x, y, width, height)
        label.raise_()


class StampView(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("stampPage")
        self.number_placement = {"x": 90, "y": 1, "scale": 80}
        self.received_placement = {"x": 90, "y": 95, "scale": 100}

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

        self.number_position_label = QLabel(
            "Across 90% · Down 1% · Size 80%"
        )
        self.number_position_label.setObjectName("positionValue")

        self.number_change_button = QPushButton("Position & Size")
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

        self.received_position_label = QLabel(
            "Across 90% · Down 95% · Size 100%"
        )
        self.received_position_label.setObjectName("positionValue")

        self.received_change_button = QPushButton("Position & Size")
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
        self.position_preview = PositionPreview()
        self.position_preview.setMinimumHeight(145)
        self.position_preview.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        paper_layout = QVBoxLayout(self.position_preview)
        paper_layout.setContentsMargins(12, 8, 12, 8)
        paper_layout.setSpacing(5)

        for width in (90, 75, 85, 65, 80, 55):
            line = QFrame()
            line.setObjectName("previewLine")
            line.setFixedSize(width, 3)
            paper_layout.addWidget(line)

        paper_layout.addStretch()

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

        self.number_change_button.clicked.connect(
            lambda: self.edit_stamp_placement(
                "Document Number",
                self.number_placement,
                self.number_position_label
            )
        )
        self.received_change_button.clicked.connect(
            lambda: self.edit_stamp_placement(
                "Received Stamp",
                self.received_placement,
                self.received_position_label
            )
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

        stamp_date = self.received_date.date()
        date_code = stamp_date.toString("yyMMdd")
        received_date = stamp_date.toString("yyyy/MM/dd")

        self.position_preview.number_stamp.setText(
            f"2300A-{date_code}-{number:03d}"
        )
        self.position_preview.received_stamp.setText(
            f"收 文\n{received_date}"
        )
        self.position_preview.set_placements(
            self.number_placement,
            self.received_placement
        )

    def edit_stamp_placement(
        self, title, placement, position_label
    ):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{title} Position and Size")

        form = QFormLayout(dialog)
        horizontal = QSpinBox()
        horizontal.setRange(0, 100)
        horizontal.setSuffix("%")
        horizontal.setValue(placement["x"])

        vertical = QSpinBox()
        vertical.setRange(0, 100)
        vertical.setSuffix("%")
        vertical.setValue(placement["y"])

        scale = QSpinBox()
        scale.setRange(10, 300)
        scale.setSuffix("%")
        scale.setValue(placement["scale"])

        form.addRow("Horizontal position", horizontal)
        form.addRow("Vertical position", vertical)
        form.addRow("Size", scale)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        placement.update({
            "x": horizontal.value(),
            "y": vertical.value(),
            "scale": scale.value(),
        })
        self.position_preview.set_placements(
            self.number_placement,
            self.received_placement
        )
        position_label.setText(
            f"Across {placement['x']}% · Down {placement['y']}% "
            f"· Size {placement['scale']}%"
        )

    # =====================================
    # STAMP SETTINGS
    # =====================================

    def get_stamp_settings(self):
        return {
            "start_number": self.start_number.value(),
            "received_date": self.received_date.date().toPython(),
            "stamp_settings": {
                "document_number": dict(self.number_placement),
                "received_stamp": dict(self.received_placement),
            },
        }

    def set_status(self, message):
        self.status_label.setText(message)
