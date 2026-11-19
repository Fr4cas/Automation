import codecs
import os
import sys
from datetime import datetime

from PySide6.QtCore import QObject, QProcess, QUrl
from PySide6.QtGui import QDesktopServices


class ScanController(QObject):
    def __init__(self, overview_view, settings_view):
        super().__init__()
        self.overview_view = overview_view
        self.settings_view = settings_view

        self.project_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.scan_script = os.path.join(
            self.project_dir, "scripts", "scan.py"
        )
        self.output_folder = os.path.join(
            self.project_dir, "output", "extracted_text"
        )

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_scan_output)
        self.process.finished.connect(self.on_scan_finished)
        self.process.errorOccurred.connect(self.on_scan_error)

        self._scan_active = False
        self._scan_finished = True
        self._scan_output_buffer = ""
        self._scan_current_filename = ""
        self._scan_total = 0
        self._scan_completed = 0
        self._scan_succeeded = 0
        self._scan_failed = 0
        self._scan_error_message = ""
        self._scan_output_decoder = codecs.getincrementaldecoder(
            "utf-8"
        )("replace")

    def get_overview_scan_folder(self):
        folder = self.settings_view.get_scan_folder()
        if not folder:
            return ""

        stamped_folder = os.path.join(
            self.project_dir, "output", "stamped"
        )
        if os.path.normcase(os.path.realpath(folder)) == os.path.normcase(
            os.path.realpath(stamped_folder)
        ):
            return ""

        return folder

    def refresh_scan_folder(self):
        folder = self.get_overview_scan_folder()
        if not folder or not os.path.isdir(folder):
            self.overview_view.set_scan_folder_info("", None, None)
            self.overview_view.set_waiting_count(None)
            return

        try:
            with os.scandir(folder) as entries:
                pdf_count = sum(
                    1 for entry in entries
                    if entry.is_file()
                    and entry.name.lower().endswith(".pdf")
                )
        except OSError as error:
            self.overview_view.set_scan_folder_info(
                folder,
                None,
                None,
                "Unable to read scan folder: {}".format(error)
            )
            self.overview_view.set_waiting_count(None)
            return

        self.overview_view.set_scan_folder_info(
            folder, pdf_count, datetime.now().strftime("%H:%M")
        )
        if not self._scan_active:
            self.overview_view.set_waiting_count(pdf_count)

    def start_processing(self):
        if self.process.state() != QProcess.ProcessState.NotRunning:
            return

        input_folder = self.settings_view.get_scan_folder()
        if not input_folder or not os.path.isdir(input_folder):
            self.overview_view.set_processing_finished(
                "Unavailable",
                "Configure a valid scan folder in Settings."
            )
            self.refresh_scan_folder()
            return

        try:
            with os.scandir(input_folder) as entries:
                pdf_filenames = sorted(
                    entry.name for entry in entries
                    if entry.is_file()
                    and entry.name.lower().endswith(".pdf")
                )
        except OSError as error:
            self.overview_view.set_processing_finished(
                "Unavailable",
                "Unable to read scan folder: {}".format(error)
            )
            self.refresh_scan_folder()
            return

        self._scan_active = True
        self._scan_finished = False
        self._scan_output_buffer = ""
        self._scan_current_filename = ""
        self._scan_total = len(pdf_filenames)
        self._scan_completed = 0
        self._scan_succeeded = 0
        self._scan_failed = 0
        self._scan_error_message = ""
        self._scan_output_decoder = codecs.getincrementaldecoder(
            "utf-8"
        )("replace")

        self.overview_view.set_processing_info(
            "",
            0,
            self._scan_total,
            0,
            0 if self._scan_total else None,
            "Processing"
        )
        self.overview_view.set_processing_count(0)
        self.overview_view.set_waiting_count(self._scan_total)

        self.process.setWorkingDirectory(self.project_dir)
        self.process.start(
            sys.executable,
            ["-u", self.scan_script, input_folder, self.output_folder]
        )

    def read_scan_output(self):
        output = self._scan_output_decoder.decode(
            bytes(self.process.readAllStandardOutput())
        )
        self._scan_output_buffer += output

        while "\n" in self._scan_output_buffer:
            line, self._scan_output_buffer = self._scan_output_buffer.split(
                "\n", 1
            )
            self._handle_scan_output_line(line.rstrip("\r"))

    def _handle_scan_output_line(self, line):
        if line.startswith("Processing: "):
            self._scan_current_filename = line[len("Processing: "):]
        elif line.startswith("Saved OCR text: "):
            self._scan_completed += 1
            self._scan_succeeded += 1
            self._scan_current_filename = ""
        elif line.startswith("Failed to process "):
            self._scan_completed += 1
            self._scan_failed += 1
            self._scan_current_filename = ""
        else:
            return

        progress_percent = (
            int(self._scan_completed * 100 / self._scan_total)
            if self._scan_total
            else None
        )
        self.overview_view.set_processing_info(
            self._scan_current_filename,
            self._scan_completed,
            self._scan_total,
            self._scan_succeeded,
            progress_percent,
            "Processing"
        )
        self.overview_view.set_processing_count(
            1 if self._scan_current_filename else 0
        )
        waiting = max(
            self._scan_total
            - self._scan_completed
            - (1 if self._scan_current_filename else 0),
            0
        )
        self.overview_view.set_waiting_count(waiting)

    def on_scan_finished(self, exit_code, exit_status):
        if self._scan_finished:
            return

        self.read_scan_output()
        self._scan_output_buffer += self._scan_output_decoder.decode(
            b"", final=True
        )
        if self._scan_output_buffer:
            self._handle_scan_output_line(
                self._scan_output_buffer.rstrip("\r")
            )
            self._scan_output_buffer = ""

        self._scan_finished = True
        self._scan_active = False

        if self._scan_error_message:
            status = "Unavailable"
            message = self._scan_error_message
        elif exit_code == 0 and self._scan_total == 0:
            status = "No PDFs found"
            message = None
        elif exit_code == 0 and self._scan_failed:
            status = "Finished with errors"
            message = None
        elif exit_code == 0:
            status = "Scan finished"
            message = None
        else:
            status = "Scan stopped"
            message = "Scanner exited with code {}".format(exit_code)

        self.overview_view.set_processing_finished(status, message)
        self.overview_view.set_processing_count(0)
        self.refresh_scan_folder()

    def on_scan_error(self, _error):
        if self._scan_finished:
            return

        self._scan_error_message = self.process.errorString()
        if self.process.state() == QProcess.ProcessState.NotRunning:
            self.on_scan_finished(-1, None)
        else:
            self.process.kill()

    def open_scan_folder(self):
        folder = self.get_overview_scan_folder()
        if not folder or not os.path.isdir(folder):
            self.refresh_scan_folder()
            return

        opened = QDesktopServices.openUrl(
            QUrl.fromLocalFile(folder)
        )
        if not opened:
            self.overview_view.set_scan_folder_message(
                "Could not open the configured scan folder."
            )
