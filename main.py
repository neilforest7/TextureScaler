import os
import shutil
import sys
# import time

import OpenImageIO as oiio
import PySide6
import qdarktheme
from OpenImageIO import ImageInput
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import Qt
from PySide6.QtWidgets import *

import icons_rc
from filetable_class import FileLine
from ui_texScaler import Ui_MainWindow


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def no_selection():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText('No Texture Selected\n' + 'Please use checkbox to select textures')
    msg.setWindowTitle("No Selection")
    msg.exec()


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.files = list()
        self.selected_row = list()
        self.LastStateRole = QtCore.Qt.UserRole

        self.ui.tableWidget.setColumnWidth(0, 500)
        self.ui.tableWidget.setColumnWidth(1, 30)
        self.ui.tableWidget.setColumnWidth(2, 70)
        self.ui.tableWidget.setColumnWidth(3, 70)
        self.ui.tableWidget.setColumnWidth(4, 50)
        ######################################################################
        # Generate table checkbox and LastStateRole
        ######################################################################
        self.addTableCheckbox()
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
        self.ui.execute_btn.clicked.connect(lambda: self.excute())
        self.ui.restart_btn.clicked.connect(lambda: self.restart())
        ######################################################################
        # Progress Bar
        ######################################################################
        self.ui.progressBar.hide()
        # self.ui.progressBar.setValue(0)
        # self.worker = WorkerThread()
        # self.progressbar()

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
        f = self.openFolderDir()
        if f:
            for root, dirs, files in os.walk(f, topdown=False):
                for name in files:
                    # print(os.path.join(root, name))
                    self.files.append(os.path.join(root, name))
            self.files = [fi for fi in self.files if fi.endswith(('.exr', '.png', '.jpg', '.hdr', '.tif', '.tga'))]
        if self.files:
            self.ui.path_label.setText(str(f) + r" : {0} files".format(len(self.files)))
            self.init_info(self.files)

    def addTableCheckbox(self):
        for row in range(self.ui.tableWidget.rowCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(PySide6.QtCore.Qt.ItemIsUserCheckable | PySide6.QtCore.Qt.ItemIsEnabled)
            item.setCheckState(PySide6.QtCore.Qt.Unchecked)
            item.setData(self.LastStateRole, item.checkState())
            self.ui.tableWidget.setItem(row, 1, item)

    def onCellChanged(self, row, column):
        if column == 1:
            item = self.ui.tableWidget.item(row, column)
            lastState = item.data(self.LastStateRole)
            currentState = item.checkState()
            if currentState != lastState:
                if currentState == PySide6.QtCore.Qt.Checked:
                    print("checked")
                    if row not in self.selected_row:
                        self.selected_row.append(row)
                        print(self.selected_row)
                else:
                    print("unchecked")
                    try:
                        self.selected_row.remove(row)
                        print(self.selected_row)
                    except ValueError:
                        pass
                item.setData(self.LastStateRole, currentState)

    def selectAll(self):
        self.selected_row = []
        for row in range(self.ui.tableWidget.rowCount()):
            self.selected_row.append(row)
            self.ui.tableWidget.item(row, 1).setCheckState(PySide6.QtCore.Qt.Checked)

    def selectNone(self):
        self.selected_row = []
        for row in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.item(row, 1).setCheckState(PySide6.QtCore.Qt.Unchecked)

    def setThreshold(self, size):
        if size:
            self.selected_row = []
            for f in range(self.ui.tableWidget.rowCount()):
                self.ui.tableWidget.item(f, 1).setCheckState(PySide6.QtCore.Qt.Unchecked)
                var = globals()[f'foo_{f}']
                if var.line[2] > int(size):
                    self.selected_row.append(f)
                    self.ui.tableWidget.item(f, 1).setCheckState(PySide6.QtCore.Qt.Checked)
                    self.ui.tableWidget.selectRow(f)
            print(self.selected_row)  # store row number as self.selected_row
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText('Size Threshold Not Set')
            msg.setWindowTitle("Size Threshold")
            msg.exec()
            self.ui.size_thres_entry.setFocus()

    def setResolution(self, res):
        if res:
            if self.selected_row:
                for f in self.selected_row:
                    var = globals()[f'foo_{f}']
                    var.line[5] = res
                    # print(var.line[5])
                    self.ui.tableWidget.setItem(f, 3, QTableWidgetItem(str(var.line[5])))
            else:
                no_selection()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText('Target Size Not Set')
            msg.setWindowTitle("Target Size")
            msg.exec()
            self.ui.size_res_entry.setFocus()

    def halfResolution(self, *arg):
        if self.selected_row:
            for f in self.selected_row:
                var = globals()[f'foo_{f}']
                var.line[5] = int(var.line[2] * 0.5 ** arg[0])
                self.ui.tableWidget.setItem(f, 3, QTableWidgetItem(str(var.line[5])))
        else:
            no_selection()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Open Textures", "",
                                                "Images (*.exr *.png *.jpg *.jpeg *.hdr *.tif *.tga);;All Files (*)",
                                                options=options)
        if files:
            print(files)
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

    def openFolderDir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderName = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        if folderName:
            print(folderName)
            return folderName

    def init_info(self, files):
        self.selected_row.clear()
        # globals().clear()
        # self.ui.tableWidget.clearContents()
        run = -1
        for f in files:
            img = ImageInput.open(f)
            spec = img.spec()
            run += 1
            globals()[f'foo_{run}'] = FileLine(run, filename=f, enable=0, x=spec.width, y=spec.height,
                                               tile=spec.tile_width > 0, target_x=0, target_tile=0)
            img.close()
            self.generate_table(run, globals()[f'foo_{run}'])

    def generate_table(self, r, var):
        self.ui.tableWidget.setRowCount(r + 1)
        self.ui.tableWidget.setItem(r, 0, QTableWidgetItem(var.line[0]))
        # self.ui.tableWidget.setItem(r, 1, QTableWidgetItem(int(var.line[1])))
        self.ui.tableWidget.setItem(r, 2, QTableWidgetItem(str(var.line[2])))
        self.ui.tableWidget.setItem(r, 3, QTableWidgetItem(str(var.line[5])))
        self.ui.tableWidget.setItem(r, 4, QTableWidgetItem(str(var.line[4])))
        self.ui.tableWidget.item(r, 2).setTextAlignment(Qt.AlignCenter)
        self.ui.tableWidget.item(r, 3).setTextAlignment(Qt.AlignCenter)
        self.ui.tableWidget.item(r, 4).setTextAlignment(Qt.AlignCenter)
        self.addTableCheckbox()

    def excute(self):
        print('#####################executing#########################')
        if self.selected_row:
            if self.ui.rename_old_btn.isChecked():
                for MyWindow.f in self.selected_row:
                    var = globals()[f'foo_{MyWindow.f}']
                    self.scale_image(var, 1)
                    # SEND Variable to QThread Class
                    # MyWindow.done = (MyWindow.f + 1) / len(self.selected_row)
            else:
                for f in self.selected_row:
                    var = globals()[f'foo_{f}']
                    self.scale_image(var, 0)
            msg = QMessageBox.question(self, "Success", "Scaled Texture Exported!!", QMessageBox.Open | QMessageBox.Ok)
            if msg == QMessageBox.Open:
                from subprocess import Popen
                f = os.path.realpath(globals()[f'foo_{0}'].line[0])
                Popen(f'explorer /select,{f}')
            self.selected_row = []
            self.init_info(self.files)
        else:
            no_selection()

    def scale_image(self, var, arg):
        buf = oiio.ImageBuf(var.line[0])
        spec = buf.spec()
        w = spec.width
        h = spec.height
        aspect = float(w) / float(h)
        if aspect == 1.0:
            # source image is square
            target_height = int(var.line[5])
        else:
            # source image is portrait
            target_height = int(w * var.line[5] / h)
        resized = oiio.ImageBuf(oiio.ImageSpec(var.line[5], target_height, spec.nchannels, spec.format))
        oiio.ImageBufAlgo.resize(resized, buf)  # , nthreads=-2
        ############################ User Chose Rename #########################
        if arg == 1:
            path, name = os.path.split(var.line[0])
            name, extension = os.path.splitext(name)
            new_path = os.path.join(path, 'origsize')
            try:
                os.mkdir(new_path)
            except FileExistsError:
                print("Directory ", new_path, " already exists")
            new_name = os.path.join(new_path, name + "_origSize" + extension)
            if not os.path.exists(new_name):
                shutil.copy(var.line[0], new_name)
            else:
                os.renames(new_name, new_name + '_deprecated')
                try:
                    shutil.copy(var.line[0], new_name)
                except FileExistsError:
                    print("Backup File", new_name, " already exists")
            resized.write(var.line[0])
        ############################ User Chose Overwritten #########################
        if arg == 0:
            print(var.line[0], '\n', var.line[1], '\n', var.line[5])
            resized.write(var.line[0])
        ########################## Try Catching Error from buf #######################
        if resized.geterror():
            print("oiio error:", resized.geterror())
        else:
            return 0
        buf.reset()
        resized.reset()

    def restart(self):
        self.selected_row.clear()
        self.files.clear()
        self.ui.path_label.clear()
        self.ui.rename_old_btn.setChecked(1)
        if self.ui.tableWidget.rowCount() > 0:
            for row in range(self.ui.tableWidget.rowCount()):
                self.ui.tableWidget.removeRow(self.ui.tableWidget.rowCount() - 1)

    # def progressbar(self):
    #     self.worker.start()
    #     # self.ui.progressBar.show()
    #     self.worker.percentage.connect(self.update_prg)
    #
    # def update_prg(self, val):
    #     self.ui.progressBar.setValue(val)

#
# class WorkerThread(QtCore.QThread):
#     percentage = QtCore.pyqtSignal(int)
#
#     def run(self):
#         for x in range(1000):
#             time.sleep(1)
#             self.percentage.emit(self.MyWindow.done)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(qdarktheme.load_stylesheet('light'))
    window = MyWindow()
    window.show()

    sys.exit(app.exec())
