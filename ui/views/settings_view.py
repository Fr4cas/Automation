import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QComboBox, QFrame, QFileDialog,
)


class SettingsView(QWidget):
    def __init__(self):
        super().__init__()

        # default scan folder
        self.project_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        self.default_scan_folder = os.path.join(
            self.project_dir,
            "output",
            "stamped"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Header section
        title = QLabel("Settings")
        title.setObjectName("pageTitle")

        subtitle = QLabel("Manage your application settings.")
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Folder Settings
        folder_section = QFrame()
        folder_layout = QVBoxLayout(folder_section)

        folder_title = QLabel("Folder Settings")
        folder_title.setObjectName("panelTitle")

        folder_layout.addWidget(folder_title)

        # Stamping folder
        stamping_label = QLabel("Stamping Folder")

        stamping_row = QHBoxLayout()

        self.stamping_folder = QLineEdit()
        self.stamping_folder.setPlaceholderText("Select stamping folder...")
        self.stamping_folder.setReadOnly(True)

        self.stamping_browse_button = QPushButton("Browse")
        self.stamping_browse_button.clicked.connect(self.select_stamping_folder)

        stamping_row.addWidget(self.stamping_folder)
        stamping_row.addWidget(self.stamping_browse_button)

        folder_layout.addWidget(stamping_label)
        folder_layout.addLayout(stamping_row)

        # Scan folder
        scan_label = QLabel("Scan Folder")

        scan_row = QHBoxLayout()

        self.scan_folder = QLineEdit()
        self.scan_folder.setPlaceholderText("Select scan folder...")
        self.scan_folder.setReadOnly(True)
        self.scan_folder.setText(self.default_scan_folder)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_scan_folder)

        scan_row.addWidget(self.scan_folder)
        scan_row.addWidget(self.browse_button)

        folder_layout.addWidget(scan_label)
        folder_layout.addLayout(scan_row)

        layout.addWidget(folder_section)

        # Language Settings
        language_section = QFrame()
        language_layout = QVBoxLayout(language_section)

        language_title = QLabel("Language")
        language_title.setObjectName("panelTitle")

        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "English",
            "繁體中文",
        ])

        language_layout.addWidget(language_title)
        language_layout.addWidget(self.language_combo)

        layout.addWidget(language_section)

        # Appearance Settings
        appearance_section = QFrame()
        appearance_layout = QVBoxLayout(appearance_section)

        appearance_title = QLabel("Appearance")
        appearance_title.setObjectName("panelTitle")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Light",
            "Dark",
        ])

        appearance_layout.addWidget(appearance_title)
        appearance_layout.addWidget(self.theme_combo)

        layout.addWidget(appearance_section)

        layout.addStretch()

    def select_stamping_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Stamping Folder"
        )

        if folder:
            self.stamping_folder.setText(folder)

    def get_stamping_folder(self):
        return self.stamping_folder.text()

    def select_scan_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Scan Folder"
        )

        if folder:
            self.scan_folder.setText(folder)

    def get_scan_folder(self):
        return self.scan_folder.text()