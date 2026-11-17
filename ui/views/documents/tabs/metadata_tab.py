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
        self.batch_container = QWidget()
        self.batch_container.setObjectName("batchContainer")

        self.batch_bar = QHBoxLayout(self.batch_container)
        self.batch_bar.setContentsMargins(12, 8, 12, 8)
        self.batch_bar.setSpacing(12)

        layout.addWidget(self.batch_container)

        self.batch_info = QVBoxLayout()
        self.batch_info.setSpacing(2)
        self.batch_bar.addLayout(self.batch_info, 1)

        self.batch_title = QLabel("Current Batch (Temporary)")
        self.batch_title.setObjectName("batchTitle")
        self.batch_info.addWidget(self.batch_title)

        self.batch_subtitle = QLabel("Process and manage documents in the temporary workspace.")
        self.batch_subtitle.setObjectName("batchSubtitle")
        self.batch_info.addWidget(self.batch_subtitle)
        self.batch_subtitle.setMinimumWidth(400)

        self.document_count_label = QLabel("0 documents")
        self.document_count_label.setObjectName("batchCountLabel")
        self.batch_bar.addWidget(self.document_count_label)

        separator = QFrame()
        separator.setObjectName("batchSeparator")
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.batch_bar.addWidget(separator)

        self.pending_export_label = QLabel("0 Pending Export")
        self.pending_export_label.setObjectName("batchCountLabel")
        self.batch_bar.addWidget(self.pending_export_label)

        separator = QFrame()
        separator.setObjectName("batchSeparator")
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.batch_bar.addWidget(separator)

        self.open_folder_button = QPushButton("Open Batch Folder")
        self.open_folder_button.setObjectName("batchActionButton")
        self.batch_bar.addWidget(self.open_folder_button)

        self.open_file_button = QPushButton("Open File")
        self.open_file_button.setObjectName("batchActionButton")
        self.batch_bar.addWidget(self.open_file_button)

        # Toolbar section
        self.toolbar = QHBoxLayout()
        layout.addLayout(self.toolbar)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("primaryToolbarButton")
        self.toolbar.addWidget(self.refresh_button)

        self.export_button = QPushButton("Export to Google Sheets")
        self.export_button.setObjectName("primaryToolbarButton")
        self.toolbar.addWidget(self.export_button)
        
        self.toolbar.addStretch()
        self.clear_button = QPushButton("Clear Batch")
        self.clear_button.setObjectName("dangerToolbarButton")
        self.toolbar.addWidget(self.clear_button)

        # Table section
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Footer section
        self.footer = QHBoxLayout()
        layout.addLayout(self.footer)

        # Left: Record information
        self.record_count_label = QLabel("共 0 筆資料（第 0 頁 / 共 0 頁）")
        self.record_count_label.setObjectName("footerLabel")
        self.footer.addWidget(self.record_count_label)

        self.footer.addStretch()

        # Centre: Pagination controls
        self.pagination = QHBoxLayout()
        self.footer.addLayout(self.pagination)

        self.first_page_button = self._add_pagination_button("«", "pageButton")
        self.previous_page_button = self._add_pagination_button("‹", "pageButton")
        self.current_page_button = self._add_pagination_button("1", "currentPageButton")
        self.next_page_button = self._add_pagination_button("›", "pageButton")
        self.last_page_button = self._add_pagination_button("»", "pageButton")

        self.footer.addStretch()

        # Right: Metadata information
        self.fields_label = QLabel("ⓘ  Metadata includes 13 official fields.")
        self.fields_label.setObjectName("footerLabel")
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
            QHeaderView.ResizeMode.Stretch
        )

        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.horizontalHeader().setFixedHeight(36)

    def _add_pagination_button(self, label, object_name):
        button = QPushButton(label)
        button.setObjectName(object_name)
        self.pagination.addWidget(button)
        return button