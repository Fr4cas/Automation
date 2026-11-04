from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QPushButton, QLineEdit,
    QFileDialog,
    )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Document Processor")
        self.resize(900, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(QLabel("Input folder"))

        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select input folder...")
        self.folder_input.setReadOnly(True)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.select_folder)

        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_button)

        layout.addLayout(folder_layout)

        # Process button
        self.start_button = QPushButton("Start Processing")
        self.start_button.setEnabled(False)

        layout.addWidget(self.start_button)

        

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")

        if folder:
            self.input_folder = Path(folder)
            self.folder_input.setText(str(self.input_folder))
            self.start_button.setEnabled(True)