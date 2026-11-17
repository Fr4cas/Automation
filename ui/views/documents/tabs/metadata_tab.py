from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QHeaderView, QPushButton,
    QLabel, QFrame,
)


class MetadataTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Current batch section
        self.batch_bar = QHBoxLayout()
        layout.addLayout(self.batch_bar)

        self.batch_info = QVBoxLayout()
        self.batch_info.setSpacing(2)
        self.batch_bar.addLayout(self.batch_info, 1)

        self.batch_title = QLabel("Current Batch (Temporary)")
        self.batch_info.addWidget(self.batch_title)

        self.batch_subtitle = QLabel("Process and manage documents in the temporary workspace.")
        self.batch_info.addWidget(self.batch_subtitle)
        self.batch_subtitle.setMinimumWidth(400)

        self.document_count_label = QLabel("0 documents")
        self.batch_bar.addWidget(self.document_count_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.batch_bar.addWidget(separator)

        self.pending_export_label = QLabel("0 Pending Export")
        self.batch_bar.addWidget(self.pending_export_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.batch_bar.addWidget(separator)

        self.open_folder_button = QPushButton("Open Batch Folder")
        self.batch_bar.addWidget(self.open_folder_button)

        self.open_file_button = QPushButton("Open File")
        self.batch_bar.addWidget(self.open_file_button)

        # Toolbar section
        self.toolbar = QHBoxLayout()
        layout.addLayout(self.toolbar)

        self.refresh_button = QPushButton("Refresh")
        self.toolbar.addWidget(self.refresh_button)

        self.export_button = QPushButton("Export to Google Sheets")
        self.toolbar.addWidget(self.export_button)
        
        self.toolbar.addStretch()
        self.clear_button = QPushButton("Clear Batch")
        self.toolbar.addWidget(self.clear_button)

        # Table section
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Footer section
        self.footer = QHBoxLayout()
        layout.addLayout(self.footer)

        # Left: Record information
        self.record_count_label = QLabel("共 0 筆資料（第 0 頁 / 共 0 頁）")
        self.footer.addWidget(self.record_count_label)

        self.footer.addStretch()

        # Centre: Pagination controls
        self.pagination = QHBoxLayout()
        self.footer.addLayout(self.pagination)

        self.first_page_button = QPushButton("«")
        self.pagination.addWidget(self.first_page_button)
        self.previous_page_button = QPushButton("‹")
        self.pagination.addWidget(self.previous_page_button)
        self.current_page_button = QPushButton("1")
        self.pagination.addWidget(self.current_page_button)
        self.next_page_button = QPushButton("›")
        self.pagination.addWidget(self.next_page_button)
        self.last_page_button = QPushButton("»")
        self.pagination.addWidget(self.last_page_button)

        self.footer.addStretch()

        # Right: Metadata information
        self.fields_label = QLabel("ⓘ  Metadata includes 13 official fields.")
        self.footer.addWidget(self.fields_label)

        # Table header settings
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels([
            "收文單號",
            "收文日期",
            "來文字號",
            "來文日期",
            "發文機關",
            "文別",
            "主旨",
            "收文部門",
            "說明",
            "註記",
            "識別",
            "特殊",
            "財務正本",
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.horizontalHeader().setFixedHeight(36)