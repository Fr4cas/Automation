import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from pathlib import Path

def load_stylesheet():
    project_dir = Path(__file__).resolve().parent
    styles_dir = project_dir / "ui" / "assets" / "styles"
    main_style_path = styles_dir / "main.qss"

    stylesheet = []

    for line in main_style_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if line.startswith("/* @include ") and line.endswith(" */"):
            relative_path = line[len("/* @include "):-len(" */")]
            style_path = styles_dir / relative_path

            if not style_path.is_file():
                raise FileNotFoundError(
                    f"Stylesheet not found: {style_path}"
                )

            stylesheet.append(
                style_path.read_text(encoding="utf-8")
            )

    return "\n".join(stylesheet)

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()