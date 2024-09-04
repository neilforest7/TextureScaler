import asyncio
import os
import shutil
import sys
import traceback
import logging
import time
from functools import wraps
from datetime import datetime
from operator import attrgetter

import OpenImageIO as oiio
import qdarktheme
from OpenImageIO import ImageInput

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QMessageBox, QLabel
from PySide6.QtCore import QObject, Signal, QTimer, Qt, Slot, QEvent, QPoint, QPointF
from PySide6.QtGui import QPixmap, QCursor

from filetable_class import FileLine
from resources.ui_texScaler import Ui_MainWindow

# 设置日志
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_dir, f'logs_{timestamp}.txt')
logging.basicConfig(filename=log_file, level=logging.INFO, encoding='utf-8',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 添加以下行来确保日志级别正确设置
logging.getLogger().setLevel(logging.INFO)

# 添加一个测试日志消息
logging.info("日志系统初始化完成")

def log_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            logging.info(f'执行函数: {func.__name__}')
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logging.info(f'函数 {func.__name__} 执行完毕，耗时 {execution_time:.4f} 秒')
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            error_msg = f'函数 {func.__name__} 执行出错: {str(e)}, 耗时 {execution_time:.4f} 秒'
            logging.error(error_msg)
            logging.error(traceback.format_exc())
            raise  # 重新抛出异常，以便程序可以继续处理它

    return wrapper

# TODO: Add right click preview function to table
CURRENT_PATH = os.path.dirname(__file__)
style_path = os.path.join(CURRENT_PATH, 'style', 'font.css')

BACKUP_FOLDER_NAME = "origsize"

@log_function
def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
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


class MyWindow(QMainWindow):
    update_table_signal = Signal(set)
    finish_signal = Signal(int, int, int, int)

    @log_function
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        logging.info("MyWindow 初始化开始")

        # load and set stylesheet
        with open(style_path, "r") as fh:
            self.setStyleSheet(fh.read())

        self.files = set()  # 使用集合存储标准化的路径
        self.selected_row = list()
        self.seleted_row_count = 0
        self.res_set_row_count = 0
        self.LastStateRole = QtCore.Qt.UserRole

        self.ui.tableWidget.setColumnWidth(0, 500)
        self.ui.tableWidget.setColumnWidth(1, 30)
        self.ui.tableWidget.setColumnWidth(2, 70)
        self.ui.tableWidget.setColumnWidth(3, 70)
        self.ui.tableWidget.setColumnWidth(4, 50)
        
        # Generate table checkbox and LastStateRole
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

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # 创建一个QTimer来定期处理asyncio事件
        self.async_timer = QTimer()
        self.async_timer.timeout.connect(self.process_async_events)
        self.async_timer.start(10)  # 每10毫秒处理一次

        self.original_open_file_text = self.ui.open_file_btn.text()
        self.original_open_path_text = self.ui.open_path_btn.text()

        self.finish_signal.connect(self.finish)
        self.update_table_signal.connect(self.update_table)

        self.ui.tableWidget.setMouseTracking(True)
        self.ui.tableWidget.viewport().installEventFilter(self)
        
        self.preview_label = QLabel(self)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("background-color: #2d2d2d; border: 1px solid #555;")
        self.preview_label.hide()

        logging.info("MyWindow 初始化完成")

    def process_async_events(self):
        self.loop.stop()
        self.loop.run_forever()

    def normalize_path(self, path):
        return os.path.normpath(os.path.abspath(path))

    def check_file_permission(self, file_path):
        return os.access(file_path, os.R_OK | os.W_OK)

    @log_function
    def browsefile(self):
        f = self.openFileNamesDialog()
        if f:
            new_files = set()
            no_permission_files = []
            for fi in f:
                if fi.lower().endswith(('.exr', '.png', '.jpg', '.hdr', '.tif', '.tga', '.jpeg')):
                    normalized_path = self.normalize_path(fi)
                    if self.check_file_permission(normalized_path):
                        new_files.add(normalized_path)
                    else:
                        no_permission_files.append(fi)

            unique_new_files = new_files - self.files
            self.files.update(unique_new_files)
            
            if unique_new_files:
                self.ui.path_label.setText(f"{os.path.dirname(next(iter(unique_new_files)))} : 新添加 {len(unique_new_files)} 个文件")
                print(f"新添加 {len(unique_new_files)} 个文件，总共 {len(self.files)} 个文件")
                asyncio.run_coroutine_threadsafe(self.init_info(), self.loop)
            else:
                QMessageBox.information(self, "提示", "没有新文件被添加")
            
            self.update_button_texts()

            if no_permission_files:
                QMessageBox.warning(self, "权限警告", f"以下 {len(no_permission_files)} 个文件没有读取和写入权限，已被跳过：\n" + "\n".join(no_permission_files[:10]) + ("\n..." if len(no_permission_files) > 10 else ""))

    @log_function
    def browsedir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderName = QFileDialog.getExistingDirectory(self, "选择目录", options=options)
        if folderName:
            print(f"选择的文件夹: {folderName}")
            new_files = set()
            no_permission_files = []
            for root, dirs, files in os.walk(folderName):
                # 跳过名为 BACKUP_FOLDER_NAME 的文件夹
                if BACKUP_FOLDER_NAME in dirs:
                    dirs.remove(BACKUP_FOLDER_NAME)
                for name in files:
                    if name.lower().endswith(('.exr', '.png', '.jpg', '.hdr', '.tif', '.tga', '.jpeg')):
                        file_path = self.normalize_path(os.path.join(root, name))
                        if self.check_file_permission(file_path):
                            new_files.add(file_path)
                        else:
                            no_permission_files.append(os.path.join(root, name))
            
            unique_new_files = new_files - self.files
            self.files.update(unique_new_files)

            if unique_new_files:
                self.ui.path_label.setText(f"{folderName} : 新添加 {len(unique_new_files)} 个文件")
                print(f"新添加 {len(unique_new_files)} 个文件，总共 {len(self.files)} 个文件")
                asyncio.run_coroutine_threadsafe(self.init_info(), self.loop)
            else:
                QMessageBox.information(self, "提示", "没有新文件被添加")
            
            self.update_button_texts()

            if no_permission_files:
                QMessageBox.warning(self, "权限警告", f"以下 {len(no_permission_files)} 个文件没有读取和写入权限，已被跳过：\n" + "\n".join(no_permission_files[:10]) + ("\n..." if len(no_permission_files) > 10 else ""))

    @log_function
    async def init_info(self):
        self.selected_row.clear()
        self.update_table_signal.emit(self.files)

    @Slot(set)
    @log_function
    def update_table(self, files):
        self.ui.tableWidget.setRowCount(0)  # 清空表格
        file_list = []
        for index, f in enumerate(files):
            try:
                img = ImageInput.open(f)
                if img:
                    spec = img.spec()
                    file_line = FileLine(index, filename=f, enable=0, x=spec.width, y=spec.height,
                                         tile=spec.tile_width > 0, target_x=0, target_tile=0)
                    file_list.append(file_line)
                    img.close()
                else:
                    print(f"无法打开图片: {f}")
            except Exception as e:
                print(f"处理文件 {f} 时出错: {str(e)}")
        
        # 按文件名排序
        file_list.sort(key=attrgetter('filename'))
        
        # 重新生成表格
        for index, file_line in enumerate(file_list):
            globals()[f'foo_{index}'] = file_line
            self.generate_table(index, file_line)
        
        self.ui.selected_label.show()
        print("表格生成完成")

    def generate_table(self, index, var):
        row_count = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row_count)
        self.ui.tableWidget.setItem(row_count, 0, QTableWidgetItem(var.filename))
        self.ui.tableWidget.setItem(row_count, 2, QTableWidgetItem(str(var.x)))
        self.ui.tableWidget.setItem(row_count, 3, QTableWidgetItem(str(var.target_x)))
        self.ui.tableWidget.setItem(row_count, 4, QTableWidgetItem(str(var.tile)))
        self.ui.tableWidget.item(row_count, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget.item(row_count, 3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableWidget.item(row_count, 4).setTextAlignment(QtCore.Qt.AlignCenter)
        
        # 添加复选框
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)
        item.setData(self.LastStateRole, item.checkState())
        self.ui.tableWidget.setItem(row_count, 1, item)

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
                item.setData(self.LastStateRole, currentState)
                self.update_selected_rows()
        self.ui.selected_label.setText(f'已选择图片: {len(self.selected_row)}')

    @log_function
    def selectAll(self):
        for row in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.item(row, 1).setCheckState(QtCore.Qt.Checked)
        self.update_selected_rows()

    @log_function
    def selectNone(self):
        for row in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.item(row, 1).setCheckState(QtCore.Qt.Unchecked)
        self.update_selected_rows()

    @log_function
    def setThreshold(self, size):
        threshold = 2048  # 默认阈值
        if size:
            try:
                threshold = int(size)
            except ValueError:
                print(f"无效的阈值: {size}，使用默认值2048")
        else:
            print("未设置阈值，使用默认值2048")

        for f in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.item(f, 1).setCheckState(QtCore.Qt.Unchecked)
            var = globals()[f'foo_{f}']
            if var.x > threshold:
                self.ui.tableWidget.item(f, 1).setCheckState(QtCore.Qt.Checked)
                self.ui.tableWidget.selectRow(f)
        
        self.update_selected_rows()
        self.ui.size_thres_entry.setText(str(threshold))

    @log_function
    def setResolution(self, res, label_num=int):
        if res:
            if self.selected_row:
                for f in self.selected_row:
                    var = globals()[f'foo_{f}']
                    var.target_x = res
                    self.ui.tableWidget.setItem(f, 3, QTableWidgetItem(str(res)))
                    self.ui.tableWidget.item(f, 3).setTextAlignment(QtCore.Qt.AlignCenter)
                asyncio.run_coroutine_threadsafe(self.updatelabel(), self.loop)
            else:
                self.no_selection()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText('未设置目标大小')
            msg.setWindowTitle("目标大小")
            msg.exec()
            with open(style_path, "r") as fh:
                msg.setStyleSheet(fh.read())
            self.ui.size_res_entry.setFocus()

    @log_function
    def halfResolution(self, *arg):
        if self.selected_row:
            for f in self.selected_row:
                var = globals()[f'foo_{f}']
                var.target_x = int(var.x * 0.5 ** arg[0])
                self.ui.tableWidget.setItem(f, 3, QTableWidgetItem(str(var.target_x)))
            asyncio.run_coroutine_threadsafe(self.updatelabel(), self.loop)
        else:
            self.no_selection()

    @log_function
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "打开纹理", "",
                                                "图像 (*.exr *.png *.jpg *.jpeg *.hdr *.tif *.tga);;所有文件 (*)",
                                                options=options)
        if files:
            return files

    @log_function
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "保存文件", "",
                                                  "批处理脚本 (*.bat)",
                                                  options=options)
        if fileName:
            print(fileName)
            return fileName

    @staticmethod
    @log_function
    def no_selection():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('未选择纹理\n' + '请使用复选框选择纹理')
        msg.setWindowTitle("未选择")
        with open(style_path, "r") as fh:
            msg.setStyleSheet(fh.read())
        msg.exec()

    async def updatelabel(self):
        label_num = 0
        for f in range(len(self.files)):
            if not globals()[f'foo_{f}'].target_x == 0: 
                label_num += 1
            await asyncio.sleep(0)
        self.ui.res_set_label.setText(f'已设置目标分辨率: {label_num} 张图片')
        self.ui.res_set_label.show()
        self.ui.groupBox.adjustSize()

    def progressbar(self, pgrs):
        self.ui.progressBar.show()
        self.ui.progressBar.setTextVisible(1)
        self.ui.progressBar.setValue(pgrs)

    @log_function
    def worker_to_execute(self):
        # 在执行操作前更新选中的行
        self.update_selected_rows()
        asyncio.run_coroutine_threadsafe(self.execute(), self.loop)

    @log_function
    def update_selected_rows(self):
        self.selected_row = []
        for row in range(self.ui.tableWidget.rowCount()):
            if self.ui.tableWidget.item(row, 1).checkState() == Qt.Checked:
                self.selected_row.append(row)
        logging.info(f"更新选中的行: {len(self.selected_row)} 行被选中")
        self.ui.selected_label.setText(f'已选择图片: {len(self.selected_row)}')

    @log_function
    async def execute(self):
        logging.info('=' * 80)
        logging.info(f'开始执行批处理操作 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        logging.info('=' * 80)
        print('#####################执行中#########################')
        
        if not self.selected_row:
            QMessageBox.warning(self, "错误", "请先选择至少一个文件")
            return
        
        total_files = len(self.selected_row)
        processed_files = 0
        successful_files = 0
        failed_files = 0
        self.processed_files_set = set()

        for row in self.selected_row:
            file_path = self.ui.tableWidget.item(row, 0).text()
            target_size = self.ui.tableWidget.item(row, 3).text()
            
            if not target_size or target_size == '0':
                continue
            
            processed_files += 1
            success = await self.scale_image(globals()[f'foo_{row}'], 1)
            if success:
                successful_files += 1
                self.processed_files_set.add(self.normalize_path(file_path))
            else:
                failed_files += 1

            progress = (processed_files / total_files) * 100
            self.progressbar(progress)

        logging.info('=' * 80)
        logging.info(f'批处理操作完成: 总文件数 {total_files}, 处理文件数 {processed_files}, 成功 {successful_files}, 失败 {failed_files}')
        logging.info(f'结束执行批处理操作 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        logging.info('=' * 80)
        self.finish_signal.emit(total_files, processed_files, successful_files, failed_files)

    @Slot(int, int, int, int)
    @log_function
    def finish(self, total_files, processed_files, successful_files, failed_files):
        result_message = f"处理结果:\n\n" \
                         f"总文件数: {total_files}\n" \
                         f"处理的文件数: {processed_files}\n" \
                         f"成功处理的文件数: {successful_files}\n" \
                         f"处理失败的文件数: {failed_files}"
        
        msg = QMessageBox(self)
        msg.setWindowTitle("处理完成")
        msg.setText(result_message)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Open | QMessageBox.Ok)
        
        ret = msg.exec()
        if ret == QMessageBox.Open:
            if self.files:
                from subprocess import Popen
                f = os.path.realpath(next(iter(self.files)))
                Popen(f'explorer /select,"{f}"')
        
        self.reload_and_update_table()

    @log_function
    def reload_and_update_table(self):
        if self.files:
            if hasattr(self, 'processed_files_set'):
                processed_files = self.processed_files_set
            else:
                processed_files = set()

            unprocessed_files = self.files - processed_files

            if unprocessed_files:
                self.files = unprocessed_files
                self.update_table(self.files)
            else:
                print("所有文件都已处理完毕")
                QMessageBox.information(self, "处理完成", "所有文件都已处理完毕")
                self.restart()
                return
        else:
            print("没有文件需要重新加载")

        self.update_button_texts()

    @log_function
    def restart(self):
        self.selected_row.clear()
        self.files.clear()
        self.ui.path_label.clear()
        self.ui.rename_old_btn.setChecked(1)
        self.ui.overwrite_btn.setChecked(0)
        self.ui.tableWidget.setRowCount(0)
        self.ui.res_set_label.hide()
        self.ui.selected_label.hide()
        self.ui.groupBox.adjustSize()
        self.update_button_texts()
        if hasattr(self, 'processed_files_set'):
            del self.processed_files_set

    @log_function
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

    @log_function
    def update_button_texts(self):
        if self.files:
            self.ui.open_file_btn.setText("Add Images...")
            self.ui.open_path_btn.setText("Add Directory...")
        else:
            self.ui.open_file_btn.setText(self.original_open_file_text)
            self.ui.open_path_btn.setText(self.original_open_path_text)

    @log_function
    async def scale_image(self, var, arg):
        try:
            print(f"开始处理文件: {var.filename}")
            buf = oiio.ImageBuf(var.filename)
            if not buf.has_error:
                spec = buf.spec()
                w = spec.width
                h = spec.height
                aspect = float(w) / float(h)
                if not w == var.target_x:
                    if aspect == 1.0:
                        target_height = int(var.target_x)
                    else:
                        target_height = int(h * var.target_x / w)
                    print(f"调整大小: {w}x{h} -> {var.target_x}x{target_height}")
                    logging.info(f"正在对文件{var.filename}进行调整大小")
                    logging.info(f"调整大小: {w}x{h} -> {var.target_x}x{target_height}")
                    resized = oiio.ImageBuf(oiio.ImageSpec(var.target_x, target_height, spec.nchannels, spec.format))
                    if not oiio.ImageBufAlgo.resize(resized, buf):
                        error_msg = f"调整大小失败: {oiio.geterror()}"
                        print(error_msg)
                        QMessageBox.critical(self, "错误", error_msg)
                        return False
                    
                    if arg == 1:
                        path, name = os.path.split(var.filename)
                        name, extension = os.path.splitext(name)
                        new_path = os.path.join(path, BACKUP_FOLDER_NAME)
                        try:
                            os.mkdir(new_path)
                        except FileExistsError:
                            pass
                        try:
                            shutil.copy(var.filename, new_path)
                            print(f"已备份原文件到: {new_path}")
                        except Exception as e:
                            print(f"备份文件时出错: {str(e)}")
                    
                    write_success = await asyncio.to_thread(lambda: resized.write(var.filename))
                    if not write_success:
                        error_msg = f"写入文件失败: {oiio.geterror()}"
                        print(error_msg)
                        print(f"文件路径: {var.filename}")
                        print(f"文件权限: {oct(os.stat(var.filename).st_mode)[-3:]}")
                        print(f"目录权限: {oct(os.stat(os.path.dirname(var.filename)).st_mode)[-3:]}")
                        QMessageBox.critical(self, "错误", error_msg)
                        return False
                    
                    print(f"成功处理并保存文件: {var.filename}")
                    return True
                else:
                    print(f"文件 {var.filename} 不需要调整大小")
                    return False
            else:
                error_msg = f"无法打开文件 {var.filename}: {buf.geterror()}"
                print(error_msg)
                QMessageBox.critical(self, "错误", error_msg)
                return False
        except Exception as e:
            error_msg = f"处理文件 {var.filename} 时发生异常: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            QMessageBox.critical(self, "错误", error_msg)
            return False
        finally:
            if 'buf' in locals():
                buf.clear()
            if 'resized' in locals():
                resized.clear()

    def eventFilter(self, source, event):
        if source == self.ui.tableWidget.viewport():
            if event.type() == QEvent.MouseMove:
                pos = event.position().toPoint()  # 使用 position() 替代 pos()
                item = self.ui.tableWidget.itemAt(pos)
                if item and item.column() == 0:  # 确保鼠标在第一列(文件名列)
                    self.show_preview(item)
                else:
                    self.hide_preview()
            elif event.type() == QEvent.Leave:
                self.hide_preview()
        return super().eventFilter(source, event)

    def show_preview(self, item):
        file_path = item.text()
        if os.path.exists(file_path):
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.preview_label.setPixmap(scaled_pixmap)
                self.preview_label.adjustSize()
                
                # 获取鼠标的全局位置
                cursor_pos = self.ui.tableWidget.mapToGlobal(self.ui.tableWidget.viewport().mapFromGlobal(QCursor.pos()))
                
                # 获取屏幕分辨率并计算缩放因子
                screen = QApplication.primaryScreen().geometry()
                scale_factor = min(screen.width() / 1920, screen.height() / 1080)
                
                # 计算缩放后的偏移量
                offset_x = int(-230 * scale_factor)
                offset_y = int(-150 * scale_factor)
                
                # 计算预览图的位置
                preview_pos = cursor_pos + QPoint(offset_x - self.preview_label.width(), offset_y - self.preview_label.height())
                
                # 确保预览图不会超出屏幕边界
                if preview_pos.x() < screen.left():
                    preview_pos.setX(cursor_pos.x() + 10)
                if preview_pos.y() < screen.top():
                    preview_pos.setY(cursor_pos.y() + 10)
                
                print(f"Screen resolution: {screen.width()}x{screen.height()}")
                print(f"Scale factor: {scale_factor}")
                print(f"Cursor position: {cursor_pos}")
                print(f"Preview position: {preview_pos}")
                print(f"Preview size: {self.preview_label.width()}x{self.preview_label.height()}")
                
                self.preview_label.move(preview_pos)
                self.preview_label.show()

    def hide_preview(self):
        self.preview_label.hide()


if __name__ == '__main__':
    logging.info("程序启动")
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(qdarktheme.load_stylesheet('light'))
    window = MyWindow()

    window.show()

    logging.info("主窗口显示")

    sys.exit(app.exec())
