from ui.views.documents.tabs.metadata_tab import MetadataTab
from ui.views.documents.tabs.rename_tab import RenameTab

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget,
)


class DocumentsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.tabs = QTabWidget()

        self.metadata_tab = MetadataTab()
        self.rename_tab = RenameTab()

        self.tabs.addTab(self.metadata_tab, "Metadata")
        self.tabs.addTab(self.rename_tab, "Rename")

        layout.addWidget(self.tabs)