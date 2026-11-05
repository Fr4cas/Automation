from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class OverviewView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Welcome back!")
        layout.addWidget(title)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = OverviewView()
    window.setWindowTitle("RYŪSEN - Overview Test")
    window.resize(900, 650)
    window.show()

    sys.exit(app.exec())