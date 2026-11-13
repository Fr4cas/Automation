import sys
import os

from ui.widgets.sidebar import Sidebar
from ui.views.overview_view import OverviewView
from ui.views.analytics_view import AnalyticsView
from ui.views.activity_view import ActivityView
from ui.views.stamped_view import StampedView
from ui.views.documents_view import DocumentsView
from ui.views.settings_view import SettingsView
from ui.views.stamp_view import StampView

from controllers.stamp_controller import StampController

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QStackedWidget,
    )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Processing
        self.process = QProcess(self)

        self.project_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.split_script = os.path.join(
            self.project_dir,
            "scripts",
            "split.py"
        )

        self.setWindowTitle("Document Processor")
        self.resize(1100, 750)
        self.setMinimumSize(1000, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Main content
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # View container
        self.view_stack = QStackedWidget()
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
        self.stamp_controller = StampController(
            self.stamp_view,
            self.settings_view
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
            self.start_processing
        )

        main_layout.addWidget(content_widget)

    def start_processing(self):
        folder = self.settings_view.get_input_folder()

        if not folder or not os.path.isdir(folder):
            return

        self.process.setWorkingDirectory(self.project_dir)

        self.process.start(
            sys.executable,
            [self.split_script, folder]
        )