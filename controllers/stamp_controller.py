from PySide6.QtCore import QObject, QThread, Signal, Slot
from pathlib import Path
from datetime import datetime

from scripts.stamp import stamp_documents


class StampWorker(QObject):
    finished = Signal(int)
    error = Signal(str)

    def __init__(self, folder, start_number, received_date):
        super().__init__()

        self.folder = folder
        self.start_number = start_number
        self.received_date = received_date

    @Slot()
    def run(self):
        try:
            processed = stamp_documents(
                self.folder,
                self.start_number,
                self.received_date
            )

            self.finished.emit(processed)

        except Exception as e:
            self.error.emit(str(e))


class StampController(QObject):
    stamping_completed = Signal()
    def __init__(self, stamp_view, settings_view):
        super().__init__()

        self.stamp_view = stamp_view
        self.settings_view = settings_view

        self.thread = None
        self.worker = None

        self.stamp_view.start_button.clicked.connect(
            self.start_stamping
        )

    def start_stamping(self):
        folder = self.settings_view.get_stamping_folder()
        settings = self.stamp_view.get_stamp_settings()

        if not folder:
            self.stamp_view.set_status(
                "Please select a stamping folder in Settings."
            )
            return

        if self.thread is not None:
            return

        self.thread = QThread()
        self.worker = StampWorker(
            folder,
            settings["start_number"],
            settings["received_date"]
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.on_stamping_finished)
        self.worker.error.connect(self.on_stamping_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.on_thread_finished)

        self.stamp_view.start_button.setEnabled(False)
        self.stamp_view.set_status("Stamping documents...")

        self.thread.start()

    def on_stamping_finished(self, processed):
        self.stamp_view.set_status(
            f"Successfully stamped {processed} documents."
        )
        
        self.stamping_completed.emit()

    def on_stamping_error(self, message):
        self.stamp_view.set_status(
            f"Stamping failed: {message}"
        )

    def on_thread_finished(self):
        self.stamp_view.start_button.setEnabled(True)

        self.thread.deleteLater()
        self.thread = None
        self.worker = None

class StampedController(QObject):
    def __init__(self, stamped_view):
        super().__init__()

        self.stamped_view = stamped_view

        self.output_folder = (
            Path(__file__).resolve().parent.parent
            / "output"
            / "stamped"
        )

        self.refresh_files()

    def refresh_files(self):
        self.output_folder.mkdir(parents=True, exist_ok=True)

        files = []

        for file in sorted(self.output_folder.glob("*.pdf")):
            modified = datetime.fromtimestamp(
                file.stat().st_mtime
            ).strftime("%Y-%m-%d %H:%M")

            files.append({
                "name": file.name,
                "modified": modified
            })

        self.stamped_view.set_files(files)