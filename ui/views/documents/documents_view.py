from ui.views.documents.tabs.metadata_tab import MetadataTab
from ui.views.documents.tabs.rename_tab import RenameTab

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget,
    QLabel,
)


class DocumentsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Page header
        self.title = QLabel("Processed Documents")
        self.title.setObjectName("pageTitle")
        layout.addWidget(self.title)

        self.subtitle = QLabel(
            "Review and edit document metadata, then export to Google Sheets."
        )
        self.subtitle.setObjectName("pageSubtitle")
        layout.addWidget(self.subtitle)

        self.tabs = QTabWidget()

        self.metadata_tab = MetadataTab()
        self.rename_tab = RenameTab()

        self.tabs.addTab(self.metadata_tab, "Metadata")
        self.tabs.addTab(self.rename_tab, "Rename")

        layout.addWidget(self.tabs)