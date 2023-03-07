import math
import os
import shutil
import sys
import time
import traceback

import OpenImageIO as oiio
import qdarktheme
from OpenImageIO import ImageInput

from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import Qt
from PySide6.QtWidgets import *
from PySide6.QtCore import QThreadPool, QRunnable, QObject, Slot, Signal

from filetable_class import FileLine
from ui_texScaler import Ui_MainWindow

from wrappers import func_timer

# TODO: Add right click preview function to table
CURRENT_PATH = os.path.dirname(__file__)
style_path = os.path.join(CURRENT_PATH, 'style', 'font.css')


def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress
    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(float)


class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        # load and set stylesheet
        with open(style_path, "r") as fh:
            self.setStyleSheet(fh.read())

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.files = list()
        self.selected_row = list()
        self.seleted_row_count = 0
        self.res_set_row_count = 0
        self.LastStateRole = QtCore.Qt.UserRole

        self.ui.tableWidget.setColumnWidth(0, 500)
        self.ui.tableWidget.setColumnWidth(1, 30)
        self.ui.tableWidget.setColumnWidth(2, 70)
        self.ui.tableWidget.setColumnWidth(3, 70)
        self.ui.tableWidget.setColumnWidth(4, 50)
        ######################################################################
        # Generate table checkbox and LastStateRole
        ######################################################################
        # self.addTableCheckbox()
        self.ui.tableWidget.cellChanged.connect(self.onCellChanged)
        self.ui.open_file_btn.clicked.connect(lambda: self.browsefile())
        self.ui.open_path_btn.clicked.connect(lambda: self.browsedir())
        self.ui.set_thres_btn.clicked.connect(lambda: self.setThreshold(self.ui.size_thres_entry.text()))
        self.ui.set_res_btn.clicked.connect(lambda: self.setResolution(self.ui.size_res_entry.text()))
        self.ui.res_128_btn.clicked.connect(lambda: self.setResolution(128))
        self.ui.res_256_btn.clicked.connect(lambda: self.setResolution(256))
        self.ui.res_512_btn.clicked.connect(lambda: self.setResolution(512))
        self.ui.res_1024_btn.clicked.connect(lambda: self.setResolution(1024))
        self.ui.res_2048_btn.clicked.connect(lambda: self.setResolution(2048))
        self.ui.res_4096_btn.clicked.connect(lambda: self.setResolution(4096))
        self.ui.res_half_btn.clicked.connect(lambda: self.halfResolution(int(1)))
        self.ui.res_quater_btn.clicked.connect(lambda: self.halfResolution(int(2)))
        self.ui.select_all_btn.clicked.connect(lambda: self.selectAll())
        self.ui.select_none_btn.clicked.connect(lambda: self.selectNone())
        self.ui.execute_btn.clicked.connect(lambda: self.worker_to_execute())
        self.ui.restart_btn.clicked.connect(lambda: self.restart())
        # self.ui.selected_label.setText("")
        # self.ui.res_set_label.setText("")
        self.ui.selected_label.hide()
        self.ui.res_set_label.hide()
        self.ui.groupBox.adjustSize()
        self.progressbar(0)
        self.ui.progressBar.hide()

    def browsefile(self):
        f = self.openFileNamesDialog()
        if f:
            self.files = f
            self.files = [fi for fi in self.files if fi.endswith(('.exr', '.png', '.jpg', '.hdr', '.tif', '.tga'))]
        if self.files:
            self.ui.path_label.setText(os.path.dirname(self.files[0]) + r" : {0} files".format(len(self.files)))
            self.init_info(self.files)

    def browsedir(self):
        self.files.clear()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderName = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        if folderName:
            print(folderName)
            f = folderName
            if f:
                for root, dirs, files in os.walk(f, topdown=False):
                    for name in files:
                        # print(os.path.join(root, name))
                        self.files.append(os.path.join(root, name))
                self.files = [fi for fi in self.files if fi.endswith(('.exr', '.png', '.jpg', '.hdr', '.tif', '.tga'))]
            if self.files:
                self.ui.path_label.setText(str(f) + f"     ::::     {len(self.files)} Images")
                self.init_info(self.files)

    def init_info(self, files):
        self.selected_row.clear()
        for index, f in enumerate(files):
            img = ImageInput.open(f)
            spec = img.spec()
            globals()[f'foo_{index}'] = FileLine(index, filename=f, enable=0, x=spec.width, y=spec.height,
                                                 tile=spec.tile_width > 0, target_x=0, target_tile=0)
            img.close()
            self.generate_table(index, globals()[f'foo_{index}'])
        self.ui.selected_label.show()

    def addTableCheckbox(self):
        for row in range(self.ui.tableWidget.rowCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setData(self.LastStateRole, item.checkState())
            self.ui.tableWidget.setItem(row, 1, item)

    def onCellChanged(self, row, column):
        if column == 1:
            item = self.ui.tableWidget.item(row, column)
            lastState = item.data(self.LastStateRole)
            currentState = item.checkState()
            if currentState != lastState:
                if currentState == QtCore.Qt.Checked:
                    if row not in self.selected_row:
                        self.selected_row.append(row)
                        # print(row)
                        # print(self.selected_row)
                else:
                    try:
                        self.selected_row.remove(row)
                    except ValueError:
                        pass
                item.setData(self.LastStateRole, currentState)
        self.ui.selected_label.setText(f'Selected Images: {len(self.selected_row)}')

    def selectAll(self):
        self.selected_row = []
        for row in range(self.ui.tableWidget.rowCount()):
            self.selected_row.append(row)
            self.ui.tableWidget.item(row, 1).setCheckState(QtCore.Qt.Checked)
        self.ui.selected_label.setText(f'Selected Images: {len(self.selected_row)}')

    def selectNone(self):
        self.selected_row = []
        for row in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.item(row, 1).setCheckState(QtCore.Qt.Unchecked)
        self.ui.selected_label.setText(f'Selected Images: {len(self.selected_row)}')

    def setThreshold(self, size):
        if size:
            self.selected_row = []
            for f in range(self.ui.tableWidget.rowCount()):
                self.ui.tableWidget.item(f, 1).setCheckState(QtCore.Qt.Unchecked)
                var = globals()[f'foo_{f}']
                if var.x > int(size):
                    self.selected_row.append(f)
                    self.ui.tableWidget.item(f, 1).setCheckState(QtCore.Qt.Checked)
                    self.ui.tableWidget.selectRow(f)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText('Size Threshold Not Set')
            msg.setWindowTitle("Size Threshold")
            msg.exec()
            with open(style_path, "r") as fh:
                msg.setStyleSheet(fh.read())
            self.ui.size_thres_entry.setFocus()

    def setResolution(self, res, label_num=int):
        if res:
            if self.selected_row:
                for f in self.selected_row:
                    var = globals()[f'foo_{f}']
                    var.target_x = res
                    self.ui.tableWidget.setItem(f, 3, QTableWidgetItem(str(res)))
                    self.ui.tableWidget.item(f, 3).setTextAlignment(Qt.AlignCenter)
                updater = Worker(self.updatelabel)
                self.threadpool.start(updater)
            else:
                self.no_selection()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText('Target Size Not Set')
            msg.setWindowTitle("Target Size")
            msg.exec()
            with open(style_path, "r") as fh:
                msg.setStyleSheet(fh.read())
            self.ui.size_res_entry.setFocus()

    def halfResolution(self, *arg):
        if self.selected_row:
            for f in self.selected_row:
                var = globals()[f'foo_{f}']
                var.target_x = int(var.x * 0.5 ** arg[0])
                self.ui.tableWidget.setItem(f, 3, QTableWidgetItem(str(var.target_x)))
            updater = Worker(self.updatelabel)
            self.threadpool.start(updater)
        else:
            self.no_selection()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Open Textures", "",
                                                "Images (*.exr *.png *.jpg *.jpeg *.hdr *.tif *.tga);;All Files (*)",
                                                options=options)
        if files:
            # print(files)
            return files

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "Batch Script (*.bat)",
                                                  options=options)  # ;;Text Files (*.txt);;All Files (*)
        if fileName:
            print(fileName)
            return fileName

    def generate_table(self, index, var):
        self.ui.tableWidget.setRowCount(index + 1)
        self.ui.tableWidget.setItem(index, 0, QTableWidgetItem(var.filename))
        # self.ui.tableWidget.setItem(index, 1, QTableWidgetItem(int(var.enable)))
        self.ui.tableWidget.setItem(index, 2, QTableWidgetItem(str(var.x)))
        self.ui.tableWidget.setItem(index, 3, QTableWidgetItem(str(var.target_x)))
        self.ui.tableWidget.setItem(index, 4, QTableWidgetItem(str(var.tile)))
        self.ui.tableWidget.item(index, 2).setTextAlignment(Qt.AlignCenter)
        self.ui.tableWidget.item(index, 3).setTextAlignment(Qt.AlignCenter)
        self.ui.tableWidget.item(index, 4).setTextAlignment(Qt.AlignCenter)
        self.addTableCheckbox()

    @staticmethod
    def no_selection():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('No Texture Selected\n' + 'Please use checkbox to select textures')
        msg.setWindowTitle("No Selection")
        # load and set stylesheet
        with open(style_path, "r") as fh:
            msg.setStyleSheet(fh.read())
        msg.exec()

    def updatelabel(self, progress_callback):
        label_num = 0
        for f in range(len(self.files)):
            if not globals()[f'foo_{f}'].target_x == 0: label_num += 1
            self.ui.res_set_label.setText(f'Target Resolution Set: {label_num} images')
        self.ui.res_set_label.show()
        self.ui.groupBox.adjustSize()

    def progressbar(self, pgrs):
        # Progress Bar
        self.ui.progressBar.show()
        # self.ui.progressBar.setRange(0,1000)
        self.ui.progressBar.setTextVisible(1)
        self.ui.progressBar.setValue(pgrs)

    def worker_to_execute(self):
        worker = Worker(self.excute)
        worker.signals.progress.connect(self.progressbar)
        worker.signals.result.connect(lambda: print("this is result signal"))
        worker.signals.finished.connect(lambda: self.finish())
        self.threadpool.start(worker)

    @func_timer
    def excute(self, progress_callback):
        print('#####################executing#########################')
        if self.selected_row:
            self.lockui(1)
            rename_btn = self.ui.rename_old_btn.isChecked()
            for pgrs, f in enumerate(self.selected_row):
                var = globals()[f'foo_{f}']
                self.scale_image(var, rename_btn)
                progress_callback.emit(round(pgrs+1 / len(self.selected_row) * 100))
            print("iteration finished")
            self.lockui(0)
        else:
            self.no_selection()

    def scale_image(self, var, arg):
        buf = oiio.ImageBuf(var.filename)
        spec = buf.spec()
        w = spec.width
        h = spec.height
        aspect = float(w) / float(h)
        if not w == var.target_x:
            if aspect == 1.0:
                # source image is square
                target_height = int(var.target_x)
            else:
                # source image is portrait
                target_height = int(h * var.target_x / w)
            resized = oiio.ImageBuf(oiio.ImageSpec(var.target_x, target_height, spec.nchannels, spec.format))
            oiio.ImageBufAlgo.resize(resized, buf)  # , nthreads=-2
            # User Chose Rename
            if arg == 1:
                path, name = os.path.split(var.filename)
                name, extension = os.path.splitext(name)
                new_path = os.path.join(path, 'origsize')
                try:
                    os.mkdir(new_path)
                except FileExistsError:
                    # print("Directory ", new_path, " already exists")
                    pass
                try:
                    shutil.copy(var.filename, new_path)
                except FileExistsError:
                    print(f"Backup File {name} in {new_path} already exists")
                except PermissionError:
                    print("Permission denied.")
                except:
                    print("Error occurred while copying file.")
                resized.write(var.filename)
            # User Chose Overwritten
            if arg == 0:
                resized.write(var.filename)
            # Try Catching Error from buf
            if resized.geterror():
                print("oiio error:", resized.geterror())
            else:
                return 1
        else:
            return 0
        buf.reset()
        resized.reset()

    def finish(self):
        msg = QMessageBox.question(self, "Success", "Scaled Texture Exported!!", QMessageBox.Open | QMessageBox.Ok)
        if msg == QMessageBox.Open:
            from subprocess import Popen
            f = os.path.realpath(globals()[f'foo_{0}'].filename)
            Popen(f'explorer /select,{f}')
        self.selected_row.clear()
        self.init_info(self.files)
        self.ui.progressBar.reset()
        self.ui.progressBar.hide()
        self.ui.res_set_label.hide()
        self.ui.selected_label.hide()
        self.ui.groupBox.adjustSize()

    def restart(self):
        self.selected_row.clear()
        self.files.clear()
        self.ui.path_label.clear()
        self.ui.rename_old_btn.setChecked(1)
        if self.ui.tableWidget.rowCount() > 0:
            for row in range(self.ui.tableWidget.rowCount()):
                self.ui.tableWidget.removeRow(self.ui.tableWidget.rowCount() - 1)
        self.ui.res_set_label.hide()
        self.ui.selected_label.hide()
        self.ui.groupBox.adjustSize()

    def lockui(self, state):
        self.ui.execute_btn.setDisabled(state)
        self.ui.frame_3.setDisabled(state)
        self.ui.frame_4.setDisabled(state)
        self.ui.rename_old_btn.setDisabled(state)
        self.ui.overwrite_btn.setDisabled(state)
        if state:
            self.ui.rename_old_btn.hide()
            self.ui.overwrite_btn.hide()
        else:
            self.ui.rename_old_btn.show()
            self.ui.overwrite_btn.show()
        self.ui.frame_10.adjustSize()
        self.ui.progressBar.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(qdarktheme.load_stylesheet('light'))
    window = MyWindow()

    window.show()

    sys.exit(app.exec())
