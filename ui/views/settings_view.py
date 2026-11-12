from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QComboBox, QFrame, QFileDialog,
)


class SettingsView(QWidget):
    def __init__(self):
        super().__init__()

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

        input_label = QLabel("Input Folder")

        input_row = QHBoxLayout()

        self.input_folder = QLineEdit()
        self.input_folder.setPlaceholderText("Select input folder...")
        self.input_folder.setReadOnly(True)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_input_folder)

        input_row.addWidget(self.input_folder)
        input_row.addWidget(self.browse_button)

        folder_layout.addWidget(input_label)
        folder_layout.addLayout(input_row)

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


    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Input Folder"
        )

        if folder:
            self.input_folder.setText(folder)

    def get_input_folder(self):
        return self.input_folder.text()