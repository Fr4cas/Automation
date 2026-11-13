from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame,
    QComboBox, QTableWidget, QTableWidgetItem, 
    QHeaderView
)


class StampedView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        title = QLabel("Stamped Documents")
        title.setObjectName("pageTitle")

        subtitle = QLabel("View, manage, and print stamped PDF files.")
        subtitle.setObjectName("pageSubtitle")

        # Page Header
        header_layout = QHBoxLayout()

        # Title and subtitle
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        # Action Buttons
        self.open_button = QPushButton("Open")
        self.rename_button = QPushButton("Rename")
        self.delete_button = QPushButton("Delete")
        self.print_button = QPushButton("Print")

        self.open_button.setObjectName("secondaryButton")
        self.rename_button.setObjectName("secondaryButton")
        self.delete_button.setObjectName("secondaryButton")
        self.print_button.setObjectName("primaryButton")

        header_layout.addWidget(self.open_button)
        header_layout.addWidget(self.rename_button)
        header_layout.addWidget(self.delete_button)
        header_layout.addSpacing(12)
        header_layout.addWidget(self.print_button)

        layout.addLayout(header_layout)

        # Main Content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)

        # Left: File List Panel
        self.file_panel = QFrame()
        self.file_panel.setObjectName("panel")

        file_layout = QVBoxLayout(self.file_panel)

        # File Table
        self.file_table = QTableWidget(0, 3)
        self.file_table.setHorizontalHeaderLabels([
            "",
            "File Name ▲",
            "Modified"
        ])

        header = self.file_table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)

        self.file_table.setColumnWidth(0, 30)
        self.file_table.setColumnWidth(2, 95)

        self.file_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.file_table.verticalHeader().setVisible(False)
        self.file_table.setShowGrid(False)

        file_layout.addWidget(self.file_table)

        # File List Footer
        footer_layout = QHBoxLayout()

        self.selected_count_label = QLabel("0 selected")
        self.file_count_label = QLabel("0 files")

        footer_layout.addWidget(self.selected_count_label)
        footer_layout.addStretch()
        footer_layout.addWidget(self.file_count_label)

        file_layout.addLayout(footer_layout)

        # Right: PDF Preview Panel
        self.preview_panel = QFrame()
        self.preview_panel.setObjectName("panel")

        preview_layout = QVBoxLayout(self.preview_panel)

        # PDF Preview Area
        self.pdf_preview = QFrame()
        self.pdf_preview.setObjectName("pdfPreview")

        pdf_preview_layout = QVBoxLayout(self.pdf_preview)

        # PDF Viewer Toolbar
        viewer_toolbar = QHBoxLayout()
        viewer_toolbar.setSpacing(8)

        # Document information
        self.pdf_icon = QLabel("PDF")

        file_info_layout = QVBoxLayout()
        file_info_layout.setSpacing(0)

        self.preview_filename = QLabel("No document selected")
        self.preview_filename.setObjectName("previewFilename")
        self.preview_filename.setMinimumWidth(155)

        self.file_info_label = QLabel("0 pages  |  0 MB")
        self.file_info_label.setMinimumWidth(155)

        file_info_layout.addWidget(self.preview_filename)
        file_info_layout.addWidget(self.file_info_label)

        viewer_toolbar.addWidget(self.pdf_icon)
        viewer_toolbar.addLayout(file_info_layout)

        viewer_toolbar.addStretch()

        # Page navigation
        self.previous_page_button = QPushButton("‹")
        self.page_label = QLabel("0 / 0")
        self.next_page_button = QPushButton("›")

        self.previous_page_button.setFixedSize(40, 34)
        self.next_page_button.setFixedSize(40, 34)

        viewer_toolbar.addWidget(self.previous_page_button)
        viewer_toolbar.addWidget(self.page_label)
        viewer_toolbar.addWidget(self.next_page_button)

        # Zoom controls
        self.zoom_out_button = QPushButton("−")
        self.zoom_label = QLabel("100%")
        self.zoom_in_button = QPushButton("+")

        self.zoom_out_button.setFixedSize(40, 34)
        self.zoom_in_button.setFixedSize(40, 34)

        viewer_toolbar.addWidget(self.zoom_out_button)
        viewer_toolbar.addWidget(self.zoom_label)
        viewer_toolbar.addWidget(self.zoom_in_button)

        # Fullscreen
        self.fullscreen_button = QPushButton("⛶")
        self.fullscreen_button.setFixedSize(40, 34)
        viewer_toolbar.addWidget(self.fullscreen_button)

        for button in (
            self.previous_page_button,
            self.next_page_button,
            self.zoom_out_button,
            self.zoom_in_button,
            self.fullscreen_button
        ):
            button.setStyleSheet("padding: 0px;")
            button.setObjectName("viewerButton")

        preview_layout.addLayout(viewer_toolbar)

        self.preview_placeholder = QLabel("Select a document to preview")
        self.preview_placeholder.setAlignment(Qt.AlignCenter)

        pdf_preview_layout.addWidget(self.preview_placeholder)

        preview_layout.addWidget(self.pdf_preview)

        self.file_panel.setMinimumWidth(320)
        self.preview_panel.setMinimumWidth(400)

        content_layout.addWidget(self.file_panel, 3)
        content_layout.addWidget(self.preview_panel, 5)

        layout.addLayout(content_layout, 1)