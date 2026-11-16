from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QHeaderView,
)


class MetadataTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Table section
        self.table = QTableWidget()
        layout.addWidget(self.table)

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
            "簽別",
            "特殊",
            "財務正本",
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.horizontalHeader().setFixedHeight(36)