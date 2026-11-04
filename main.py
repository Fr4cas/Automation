import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from pathlib import Path

def load_stylesheet():
    project_dir = Path(__file__).resolve().parent
    styles_dir = project_dir / "ui" / "assets" / "styles"

    common_style_path = styles_dir / "common.qss"
    light_style_path = styles_dir / "light.qss"

    common_style = common_style_path.read_text(encoding="utf-8")
    light_style = light_style_path.read_text(encoding="utf-8")

    return common_style + "\n" + light_style

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()