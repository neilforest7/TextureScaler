import sys
import time
import asyncio
from PySide6.QtCore import (Qt, Signal, Slot, QObject, QThread)
from PySide6.QtWidgets import (QApplication, QProgressBar, QWidget, QHBoxLayout, QPushButton, QMainWindow, QDialog)
from asyncqt import (QEventLoop, QThreadExecutor)


class MainWindow(QMainWindow):
    """Main window, with one button for exporting stuff"""

    def __init__(self, parent=None):
        super().__init__(parent)
        central_widget = QWidget(self)
        layout = QHBoxLayout(self)
        button = QPushButton("Press me...")
        button.clicked.connect(self.export_stuff)
        layout.addWidget(button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def export_stuff(self):
        """Opens dialog and starts exporting"""
        some_window = MyExportDialog(self)
        some_window.exec_()


class MyAbstractExportThread(QThread):
    """Base export thread"""
    change_value = Signal(int)
    loop = asyncio.get_event_loop()

    def run(self):
        cnt = 0
        while cnt < 100:
            cnt += 1
            self.loop.run_until_complete(self.operation())
            self.change_value.emit(cnt)

    @asyncio.coroutine
    def operation(self):
        pass


class MyExpensiveExportThread(MyAbstractExportThread):

    @asyncio.coroutine
    def operation(self):
        """Something that takes a lot of CPU power"""
        some_val = 0
        for i in range(10000000):
            some_val += 1


class MyInexpensiveExportThread(MyAbstractExportThread):

    def operation(self):
        """Something that doesn't take a lot of CPU power"""
        time.sleep(.1)


class MyExportDialog(QDialog):
    """Dialog which does some stuff, and shows its progress"""

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint)
        self.loop = asyncio.get_event_loop()
        self.setWindowTitle("Exporting...")
        layout = QHBoxLayout()
        self.progress_bar = self._create_progress_bar()
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        # self.worker = MyInexpensiveExportThread()  # Works fine
        self.worker = MyExpensiveExportThread()  # Super laggy
        self.worker.change_value.connect(self.set_progressbar)
        self.worker.finished.connect(self.close)

        with QThreadExecutor(1) as qt_thread_executor:
            loop.run_in_executor(qt_thread_executor, self.worker.start)

    def _create_progress_bar(self):
        progress_bar = QProgressBar(self)
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        return progress_bar

    @Slot(int)
    def set_progressbar(self, value):
        self.loop.call_soon_threadsafe(self.progress_bar.setValue, value)


if __name__ == "__main__":
    app = QApplication()
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    loop.run_forever(sys.exit(app.exec_()))