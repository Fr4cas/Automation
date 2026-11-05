from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QPushButton, QLineEdit,
    QFileDialog, QProgressBar, QTextEdit,
    QFrame,
    )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Document Processor")
        self.resize(900, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        self.input_card = QFrame()
        self.input_card.setObjectName("inputCard")

        input_card_layout = QVBoxLayout(self.input_card)
        input_card_layout.setContentsMargins(20, 20, 20, 20)
        input_card_layout.setSpacing(12)
        input_card_layout.addWidget(QLabel("Input folder"))

        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select input folder...")
        self.folder_input.setReadOnly(True)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.select_folder)

        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_button)

        input_card_layout.addLayout(folder_layout)

        layout.addWidget(self.input_card)

        # Process button
        self.start_button = QPushButton("Start Processing")
        self.start_button.setObjectName("startButton")
        self.start_button.setEnabled(False)

        layout.addWidget(self.start_button)

        # Progress bar
        self.progress_card = QFrame()
        self.progress_card.setObjectName("progressCard")
        progress_card_layout = QVBoxLayout(self.progress_card)
        progress_card_layout.setContentsMargins(20, 20, 20, 20)
        progress_card_layout.setSpacing(12)

        self.progress_bar = QProgressBar()
        QProgressBar.setRange(self.progress_bar, 0, 100)

        progress_card_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Waiting to start")
        progress_card_layout.addWidget(self.status_label)

        layout.addWidget(self.progress_card)

        results_layout = QHBoxLayout()

        # Results labels
        self.results_card = QFrame()
        self.results_card.setObjectName("resultsCard")

        results_card_layout = QVBoxLayout(self.results_card)
        results_card_layout.setContentsMargins(20, 20, 20, 20)
        results_card_layout.setSpacing(12)

        results_blocks_layout = QHBoxLayout()
        results_blocks_layout.setSpacing(12)

        self.success_block = QFrame()
        self.success_block.setObjectName("successBlock")

        self.failed_block = QFrame()
        self.failed_block.setObjectName("failedBlock")

        success_block_layout = QVBoxLayout(self.success_block)
        success_block_layout.setContentsMargins(16, 16, 16, 16)
        success_block_layout.setSpacing(6)

        failed_block_layout = QVBoxLayout(self.failed_block)
        failed_block_layout.setContentsMargins(16, 16, 16, 16)
        failed_block_layout.setSpacing(6)

        self.success_title = QLabel("Success")
        self.success_label = QLabel("0")
        self.success_title.setObjectName("successTitle")
        self.success_label.setObjectName("successNumber")

        self.failed_title = QLabel("Failed")
        self.failed_label = QLabel("0")
        self.failed_title.setObjectName("failedTitle")
        self.failed_label.setObjectName("failedNumber")

        success_block_layout.addWidget(self.success_title)
        success_block_layout.addWidget(self.success_label) 

        failed_block_layout.addWidget(self.failed_title)
        failed_block_layout.addWidget(self.failed_label)

        results_blocks_layout.addWidget(self.success_block)
        results_blocks_layout.addWidget(self.failed_block)

        results_card_layout.addLayout(results_blocks_layout)

        layout.addWidget(self.results_card)
        
        # Process log
        self.log_card = QFrame()
        self.log_card.setObjectName("logCard")

        log_card_layout = QVBoxLayout(self.log_card)
        log_card_layout.setContentsMargins(20, 20, 20, 20)
        log_card_layout.setSpacing(12)

        log_card_layout.addWidget(QLabel("Processing Log"))

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        log_card_layout.addWidget(self.log_output)

        layout.addWidget(self.log_card)

        # Output and Error folder buttons
        folder_buttons = QHBoxLayout()
        self.output_button = QPushButton("Open Output Folder")
        self.error_button = QPushButton("Open Error Folder")

        self.output_button.setEnabled(False)
        self.error_button.setEnabled(False)

        folder_buttons.addWidget(self.output_button)
        folder_buttons.addWidget(self.error_button)
        layout.addLayout(folder_buttons)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")

        if folder:
            self.input_folder = Path(folder)
            self.folder_input.setText(str(self.input_folder))
            self.start_button.setEnabled(True)