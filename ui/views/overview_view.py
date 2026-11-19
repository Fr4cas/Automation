from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QScrollArea, QProgressBar, QGraphicsDropShadowEffect,
)


class _MetricIcon(QWidget):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.setFixedSize(24, 24)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("#68788D"), 1.7))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        if self.kind == "document":
            painter.drawRoundedRect(6, 3, 12, 18, 2, 2)
            painter.drawLine(9, 9, 15, 9)
            painter.drawLine(9, 13, 15, 13)
            painter.drawLine(9, 17, 13, 17)
        elif self.kind == "processing":
            painter.drawEllipse(4, 4, 16, 16)
            painter.drawArc(4, 4, 16, 16, 35 * 16, 245 * 16)
            painter.drawLine(15, 3, 20, 5)
        else:
            painter.drawEllipse(4, 4, 16, 16)
            painter.drawLine(8, 12, 11, 15)
            painter.drawLine(11, 15, 17, 9)


class OverviewView(QWidget):
    open_folder_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("overviewCanvas")
        self.setStyleSheet("""
            QWidget#overviewCanvas {
                background-color: #F6F7F9;
            }
            QLabel#overviewTitle {
                color: #1E293B;
                font-size: 22pt;
                font-weight: 600;
            }
            QLabel#overviewSubtitle {
                color: #64748B;
                font-size: 10pt;
            }
            QFrame#overviewCard, QFrame#metricCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E7ED;
                border-radius: 10px;
            }
            QLabel#panelTitle {
                color: #1E293B;
                font-size: 11pt;
                font-weight: 600;
            }
            QLabel#secondaryText, QLabel#metricDescription,
            QLabel#fieldLabel, QLabel#emptyState {
                color: #718096;
                font-size: 9pt;
            }
            QLabel#metricTitle {
                color: #64748B;
                font-size: 9pt;
                font-weight: 600;
            }
            QLabel#metricValue {
                color: #1E293B;
                font-size: 23pt;
                font-weight: 600;
            }
            QLabel#fieldValue {
                color: #334155;
                font-size: 9pt;
                font-weight: 500;
            }
            QLabel#currentFilename {
                color: #243247;
                font-size: 10pt;
                font-weight: 600;
            }
            QLabel#statusPill {
                color: #355C86;
                background-color: #EEF4FA;
                border: 1px solid #DCE7F1;
                border-radius: 9px;
                padding: 3px 9px;
                font-size: 8pt;
                font-weight: 600;
            }
            QPushButton#overviewPrimaryButton {
                color: #FFFFFF;
                background-color: #315F91;
                border: 1px solid #315F91;
                border-radius: 7px;
                padding: 9px 16px;
                font-size: 9pt;
                font-weight: 600;
            }
            QPushButton#overviewPrimaryButton:hover {
                background-color: #284F79;
            }
            QPushButton#overviewPrimaryButton:pressed {
                background-color: #234568;
            }
            QPushButton#overviewSecondaryButton {
                color: #334155;
                background-color: #FFFFFF;
                border: 1px solid #D5DCE5;
                border-radius: 7px;
                padding: 7px 12px;
                font-size: 9pt;
            }
            QPushButton#overviewSecondaryButton:disabled {
                color: #A0AAB8;
                background-color: #F7F8FA;
            }
            QProgressBar#overviewProgress {
                border: 0;
                border-radius: 4px;
                background-color: #E8EDF2;
                min-height: 8px;
                max-height: 8px;
            }
            QProgressBar#overviewProgress::chunk {
                border-radius: 4px;
                background-color: #4B78A6;
            }
        """)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setStyleSheet("QScrollArea { background: transparent; }")
        root_layout.addWidget(self.scroll_area)

        canvas = QWidget()
        canvas.setObjectName("overviewContent")
        canvas.setStyleSheet("QWidget#overviewContent { background: transparent; }")
        content_layout = QVBoxLayout(canvas)
        content_layout.setContentsMargins(2, 2, 10, 10)
        content_layout.setSpacing(14)
        self.scroll_area.setWidget(canvas)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        title_layout = QVBoxLayout()
        title_layout.setSpacing(3)

        title = QLabel("Overview")
        title.setObjectName("overviewTitle")
        subtitle = QLabel("Monitor your document scanning workflow.")
        subtitle.setObjectName("overviewSubtitle")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        self.start_button = QPushButton("Start Scanning")
        self.start_button.setObjectName("overviewPrimaryButton")
        self.start_button.setMinimumHeight(38)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.start_button)
        content_layout.addLayout(header_layout)

        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(12)
        self.waiting_value = self._add_metric(
            metrics_layout, "Waiting", "PDFs awaiting scanning", "document"
        )
        self.processing_value = self._add_metric(
            metrics_layout, "Processing", "Currently being scanned", "processing"
        )
        self.exported_value = self._add_metric(
            metrics_layout, "Exported", "Successfully exported", "exported"
        )
        content_layout.addLayout(metrics_layout)

        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(12)
        self.processing_panel, processing_layout = self._create_panel(
            "Current Processing"
        )
        self.activity_panel, activity_layout = self._create_panel(
            "Recent Activity"
        )
        panels_layout.addWidget(self.processing_panel, 3)
        panels_layout.addWidget(self.activity_panel, 2)
        content_layout.addLayout(panels_layout)

        status_layout = QHBoxLayout()
        status_layout.setSpacing(8)
        self.processing_status = QLabel("No active scan")
        self.processing_status.setObjectName("statusPill")
        status_layout.addWidget(self.processing_status)
        status_layout.addStretch()
        processing_layout.addLayout(status_layout)

        current_file_label = QLabel("Current PDF")
        current_file_label.setObjectName("fieldLabel")
        self.current_filename_label = QLabel("No active scan")
        self.current_filename_label.setObjectName("currentFilename")
        self.current_filename_label.setWordWrap(True)
        processing_layout.addWidget(current_file_label)
        processing_layout.addWidget(self.current_filename_label)

        processing_stats = QHBoxLayout()
        processing_stats.setSpacing(20)
        total_column, total_value = self._create_stat_column(
            "PDFs in this scan", "—"
        )
        success_column, self.successful_value = self._create_stat_column(
            "Successfully processed", "—"
        )
        processing_stats.addLayout(total_column)
        processing_stats.addLayout(success_column)
        processing_stats.addStretch()
        processing_layout.addLayout(processing_stats)
        self.total_value = total_value

        progress_header = QHBoxLayout()
        progress_label = QLabel("Scan progress")
        progress_label.setObjectName("fieldLabel")
        self.progress_value = QLabel("—")
        self.progress_value.setObjectName("fieldValue")
        progress_header.addWidget(progress_label)
        progress_header.addStretch()
        progress_header.addWidget(self.progress_value)
        processing_layout.addLayout(progress_header)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("overviewProgress")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        processing_layout.addWidget(self.progress_bar)

        self.activity_empty_state = QLabel(
            "No processing history is available yet."
        )
        self.activity_empty_state.setObjectName("emptyState")
        self.activity_empty_state.setWordWrap(True)
        activity_layout.addWidget(self.activity_empty_state)
        activity_layout.addStretch()

        self.batch_panel, batch_layout = self._create_panel(
            "Current Batch (Temporary)"
        )
        batch_grid = QHBoxLayout()
        batch_grid.setSpacing(22)
        self.batch_values = {}
        for label in ("Documents", "Extracted", "Exported", "Export Status"):
            column, value = self._create_stat_column(label, "—")
            batch_grid.addLayout(column)
            self.batch_values[label] = value
        batch_grid.addStretch()
        batch_layout.addLayout(batch_grid)

        batch_description = QLabel(
            "Review and finalize the documents before exporting to Google Sheets."
        )
        batch_description.setObjectName("secondaryText")
        batch_description.setWordWrap(True)
        batch_layout.addWidget(batch_description)
        batch_empty_state = QLabel(
            "No temporary document collection is available yet."
        )
        batch_empty_state.setObjectName("emptyState")
        batch_layout.addWidget(batch_empty_state)
        content_layout.addWidget(self.batch_panel)

        self.folder_panel, folder_layout = self._create_panel("Scan Folder")
        folder_row = QHBoxLayout()
        folder_details = QVBoxLayout()
        folder_details.setSpacing(4)
        self.folder_path_label = QLabel("Configure a scan folder in Settings.")
        self.folder_path_label.setObjectName("fieldValue")
        self.folder_path_label.setWordWrap(True)
        self.folder_summary_label = QLabel("PDFs detected: —    Last checked: —")
        self.folder_summary_label.setObjectName("secondaryText")
        folder_details.addWidget(self.folder_path_label)
        folder_details.addWidget(self.folder_summary_label)
        folder_row.addLayout(folder_details, 1)

        self.open_folder_button = QPushButton("Open Folder")
        self.open_folder_button.setObjectName("overviewSecondaryButton")
        self.open_folder_button.setEnabled(False)
        self.open_folder_button.clicked.connect(
            self.open_folder_requested.emit
        )
        folder_row.addWidget(self.open_folder_button)
        folder_layout.addLayout(folder_row)
        content_layout.addWidget(self.folder_panel)

        self._apply_card_shadow(self.processing_panel)
        self._apply_card_shadow(self.activity_panel)
        self._apply_card_shadow(self.batch_panel)
        self._apply_card_shadow(self.folder_panel)

    def _add_metric(self, layout, title, description, icon_kind):
        card = QFrame()
        card.setObjectName("metricCard")
        card.setMinimumHeight(112)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 12, 14, 12)
        card_layout.setSpacing(5)

        heading = QHBoxLayout()
        heading.setSpacing(8)
        icon = _MetricIcon(icon_kind)
        heading.addWidget(icon)
        title_label = QLabel(title)
        title_label.setObjectName("metricTitle")
        heading.addWidget(title_label)
        heading.addStretch()
        card_layout.addLayout(heading)

        value = QLabel("—")
        value.setObjectName("metricValue")
        description_label = QLabel(description)
        description_label.setObjectName("metricDescription")
        card_layout.addWidget(value)
        card_layout.addWidget(description_label)

        layout.addWidget(card, 1)
        self._apply_card_shadow(card)
        return value

    def _create_panel(self, title):
        panel = QFrame()
        panel.setObjectName("overviewCard")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 14, 16, 14)
        panel_layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("panelTitle")
        panel_layout.addWidget(title_label)
        return panel, panel_layout

    def _create_stat_column(self, label, value):
        column = QVBoxLayout()
        column.setSpacing(3)
        label_widget = QLabel(label)
        label_widget.setObjectName("fieldLabel")
        value_widget = QLabel(value)
        value_widget.setObjectName("fieldValue")
        column.addWidget(label_widget)
        column.addWidget(value_widget)
        return column, value_widget

    def _apply_card_shadow(self, card):
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(14)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(31, 45, 61, 14))
        card.setGraphicsEffect(shadow)

    def set_scan_folder_info(
        self, path, pdf_count, last_checked, message=None
    ):
        self.folder_path_label.setText(
            path if path else "Configure a scan folder in Settings."
        )
        self.open_folder_button.setEnabled(bool(path))

        if message:
            summary = message
        else:
            count_text = str(pdf_count) if pdf_count is not None else "—"
            checked_text = last_checked if last_checked else "—"
            summary = "PDFs detected: {}    Last checked: {}".format(
                count_text, checked_text
            )
        self.folder_summary_label.setText(summary)

    def set_processing_info(
        self, filename, completed, total, successful,
        progress_percent, status
    ):
        self.processing_status.setText(status)
        self.start_button.setEnabled(status != "Processing")
        self.current_filename_label.setText(
            filename or (
                "Preparing scan..." if status == "Processing"
                else "No active scan"
            )
        )
        self.total_value.setText(str(total))
        self.successful_value.setText(str(successful))

        if progress_percent is None:
            self.progress_value.setText("No PDFs found")
            self.progress_bar.setValue(0)
        else:
            self.progress_value.setText(
                "{}%  ({}/{} PDFs)".format(
                    progress_percent, completed, total
                )
            )
            self.progress_bar.setValue(progress_percent)

    def set_processing_finished(self, status, message=None):
        self.processing_status.setText(status)
        self.current_filename_label.setText(
            message if message else "No active scan"
        )
        self.start_button.setEnabled(True)

    def set_waiting_count(self, count):
        self.waiting_value.setText(str(count) if count is not None else "—")

    def set_processing_count(self, count):
        self.processing_value.setText(
            str(count) if count is not None else "—"
        )

    def set_exported_count(self, count):
        self.exported_value.setText(
            str(count) if count is not None else "—"
        )

    def set_temporary_batch_info(
        self, documents=None, extracted=None, exported=None,
        export_status=None
    ):
        values = {
            "Documents": documents,
            "Extracted": extracted,
            "Exported": exported,
            "Export Status": export_status,
        }
        for label, value in values.items():
            self.batch_values[label].setText(
                str(value) if value is not None else "—"
            )

    def set_scan_folder_message(self, message):
        self.folder_summary_label.setText(message)
