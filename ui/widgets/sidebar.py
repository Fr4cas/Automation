from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QHBoxLayout, QPushButton,
)


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("sidebar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(12)

        logo_layout = QHBoxLayout()

        logo_icon = QLabel()
        logo_icon.setPixmap(
            QPixmap("ui/assets/images/logo.png").scaled(
                QSize(48, 48),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        logo_layout.addWidget(logo_icon)

        layout.addLayout(logo_layout)
        layout.addSpacing(24)

        section_label = QLabel("WORKSPACE")
        section_label.setObjectName("sectionLabel")
        layout.addWidget(section_label)

        self.overview_button = QPushButton("Overview")
        self.overview_button.setObjectName("navButton")
        self.overview_button.setCheckable(True)
        self.overview_button.setChecked(True)

        layout.addWidget(self.overview_button)

        self.analytics_button = QPushButton("Analytics")
        self.analytics_button.setObjectName("navButton")

        self.activity_button = QPushButton("Activity Log")
        self.activity_button.setObjectName("navButton")

        self.stamp_button = QPushButton("Stamp")
        self.stamp_button.setObjectName("navButton")

        layout.addWidget(self.analytics_button)
        layout.addWidget(self.activity_button)
        layout.addWidget(self.stamp_button)

        layout.addSpacing(24)

        documents_label = QLabel("DOCUMENTS")
        documents_label.setObjectName("sectionLabel")
        layout.addWidget(documents_label)

        self.documents_button = QPushButton("Processed Documents")
        self.documents_button.setObjectName("navButton")

        layout.addWidget(self.documents_button)

        layout.addStretch()

        self.settings_button = QPushButton("Settings")
        self.settings_button.setObjectName("navButton")

        layout.addWidget(self.settings_button)