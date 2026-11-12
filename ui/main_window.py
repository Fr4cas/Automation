from ui.widgets.sidebar import Sidebar
from ui.views.overview_view import OverviewView
from ui.views.analytics_view import AnalyticsView

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QStackedWidget,
    )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Document Processor")
        self.resize(900, 650)

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

        # Navigation
        navigation = {
            self.sidebar.overview_button: self.overview_view,
            self.sidebar.analytics_button: self.analytics_view,
        }

        for button, view in navigation.items():
            button.clicked.connect(
                lambda checked=False, page=view:
                    self.view_stack.setCurrentWidget(page)
            )

        main_layout.addWidget(content_widget)
