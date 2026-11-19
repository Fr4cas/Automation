from ui.widgets.sidebar import Sidebar
from ui.views.overview_view import OverviewView
from ui.views.analytics_view import AnalyticsView
from ui.views.activity_view import ActivityView
from ui.views.stamped_view import StampedView
from ui.views.documents.documents_view import DocumentsView
from ui.views.settings_view import SettingsView
from ui.views.stamp_view import StampView

from controllers.scan_controller import ScanController
from controllers.stamp_controller import (StampController, StampedController)

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QStackedWidget,
    )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Document Processor")
        self.resize(1100, 750)
        self.setMinimumSize(1000, 650)

        central_widget = QWidget()
        central_widget.setObjectName("appRoot")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Main content
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")
        layout = QVBoxLayout(content_widget)

        layout.setSpacing(16)
        layout.setContentsMargins(12, 24, 12, 24)

        # View container
        self.view_stack = QStackedWidget()
        self.view_stack.setObjectName("viewStack")
        layout.addWidget(self.view_stack)

        # Overview
        self.overview_view = OverviewView()
        self.view_stack.addWidget(self.overview_view)

        # Analytics
        self.analytics_view = AnalyticsView()
        self.view_stack.addWidget(self.analytics_view)

        # Activity
        self.activity_view = ActivityView()
        self.view_stack.addWidget(self.activity_view)

        # Stamp
        self.stamp_view = StampView()
        self.view_stack.addWidget(self.stamp_view)

        # Stamped
        self.stamped_view = StampedView()
        self.view_stack.addWidget(self.stamped_view)

        # Documents
        self.documents_view = DocumentsView()
        self.view_stack.addWidget(self.documents_view)

        # Settings
        self.settings_view = SettingsView()
        self.view_stack.addWidget(self.settings_view)

        # Controllers
        self.scan_controller = ScanController(
            self.overview_view,
            self.settings_view
        )

        self.stamp_controller = StampController(
            self.stamp_view,
            self.settings_view
        )

        self.stamped_controller = StampedController(
            self.stamped_view
        )

        self.stamp_controller.stamping_completed.connect(
            self.stamped_controller.refresh_files
        )

        # Navigation
        navigation = {
            self.sidebar.overview_button: self.overview_view,
            self.sidebar.analytics_button: self.analytics_view,
            self.sidebar.activity_button: self.activity_view,
            self.sidebar.stamp_button: self.stamp_view,
            self.sidebar.stamped_button: self.stamped_view,
            self.sidebar.documents_button: self.documents_view,
            self.sidebar.settings_button: self.settings_view,
        }

        for button, view in navigation.items():
            button.clicked.connect(
                lambda checked=False, page=view:
                    self.view_stack.setCurrentWidget(page)
            )

        self.overview_view.start_button.clicked.connect(
            self.scan_controller.start_processing
        )
        self.overview_view.open_folder_requested.connect(
            self.scan_controller.open_scan_folder
        )

        self.view_stack.currentChanged.connect(self.on_view_changed)
        self.scan_controller.refresh_scan_folder()

        main_layout.addWidget(content_widget)

    def on_view_changed(self, index):
        if self.view_stack.widget(index) is self.overview_view:
            self.scan_controller.refresh_scan_folder()
