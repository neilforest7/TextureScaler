# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'texScalerNJeiJI.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import resources.icons_new_rc as icons_new_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1031, 534)
        MainWindow.setMinimumSize(QSize(1000, 0))
        font = QFont()
        font.setPointSize(10)
        font.setStyleStrategy(QFont.PreferAntialias)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setFont(font)
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFont(font)
        self.horizontalLayout_7 = QHBoxLayout(self.frame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFont(font)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 0, 9, 9)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        font1 = QFont()
        font1.setPointSize(9)
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.frame_3.setFont(font1)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 9, -1, -1)
        self.restart_btn = QPushButton(self.frame_3)
        self.restart_btn.setObjectName(u"restart_btn")
        self.restart_btn.setMinimumSize(QSize(50, 0))
        self.restart_btn.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/icons/reload 30.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.restart_btn.setIcon(icon)
        self.restart_btn.setIconSize(QSize(10, 12))

        self.horizontalLayout_2.addWidget(self.restart_btn)

        self.path_label = QLineEdit(self.frame_3)
        self.path_label.setObjectName(u"path_label")
        self.path_label.setMinimumSize(QSize(0, 25))
        self.path_label.setMaximumSize(QSize(16777215, 25))
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(False)
        font2.setStyleStrategy(QFont.PreferAntialias)
        self.path_label.setFont(font2)
        self.path_label.setDragEnabled(True)
        self.path_label.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.path_label)

        self.open_path_btn = QPushButton(self.frame_3)
        self.open_path_btn.setObjectName(u"open_path_btn")
        self.open_path_btn.setMinimumSize(QSize(84, 0))
        self.open_path_btn.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/folder-open-fill 363.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.open_path_btn.setIcon(icon1)
        self.open_path_btn.setIconSize(QSize(60, 12))

        self.horizontalLayout_2.addWidget(self.open_path_btn)

        self.open_file_btn = QPushButton(self.frame_3)
        self.open_file_btn.setObjectName(u"open_file_btn")
        self.open_file_btn.setMinimumSize(QSize(84, 0))
        self.open_file_btn.setFont(font)
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/file-copy-fill 357.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.open_file_btn.setIcon(icon2)
        self.open_file_btn.setIconSize(QSize(60, 12))

        self.horizontalLayout_2.addWidget(self.open_file_btn)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFont(font1)
        self.frame_4.setStyleSheet(u"")
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.frame_4)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem.setFont(font1);
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        font3 = QFont()
        font3.setPointSize(7)
        font3.setStyleStrategy(QFont.PreferAntialias)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem1.setFont(font3);
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem2.setFont(font1);
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem3.setFont(font1);
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem4.setFont(font1);
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)
        self.tableWidget.setMinimumSize(QSize(550, 0))
        self.tableWidget.setMaximumSize(QSize(50000, 16777215))
        self.tableWidget.setFont(font1)
        self.tableWidget.setStyleSheet(u"selection-background-color: rgb(204, 232, 255);")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setGridStyle(Qt.DashLine)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)

        self.horizontalLayout_3.addWidget(self.tableWidget)

        self.frame_6 = QFrame(self.frame_4)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy2)
        self.verticalLayout_2 = QVBoxLayout(self.frame_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.groupBox = QGroupBox(self.frame_6)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font1)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_9 = QFrame(self.groupBox)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.select_all_btn = QPushButton(self.frame_9)
        self.select_all_btn.setObjectName(u"select_all_btn")
        self.select_all_btn.setFont(font)

        self.horizontalLayout.addWidget(self.select_all_btn)

        self.select_none_btn = QPushButton(self.frame_9)
        self.select_none_btn.setObjectName(u"select_none_btn")
        self.select_none_btn.setFont(font)

        self.horizontalLayout.addWidget(self.select_none_btn)


        self.verticalLayout_5.addWidget(self.frame_9)

        self.frame_7 = QFrame(self.groupBox)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy3)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.size_thres_entry = QLineEdit(self.frame_7)
        self.size_thres_entry.setObjectName(u"size_thres_entry")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.size_thres_entry.sizePolicy().hasHeightForWidth())
        self.size_thres_entry.setSizePolicy(sizePolicy4)
        self.size_thres_entry.setMinimumSize(QSize(40, 0))
        self.size_thres_entry.setMaximumSize(QSize(50, 16777215))
        self.size_thres_entry.setFont(font1)
        self.size_thres_entry.setMaxLength(5)
        self.size_thres_entry.setAlignment(Qt.AlignCenter)
        self.size_thres_entry.setClearButtonEnabled(False)

        self.horizontalLayout_5.addWidget(self.size_thres_entry)

        self.set_thres_btn = QPushButton(self.frame_7)
        self.set_thres_btn.setObjectName(u"set_thres_btn")
        self.set_thres_btn.setFont(font)

        self.horizontalLayout_5.addWidget(self.set_thres_btn)


        self.verticalLayout_5.addWidget(self.frame_7)

        self.frame_11 = QFrame(self.groupBox)
        self.frame_11.setObjectName(u"frame_11")
        font4 = QFont()
        font4.setFamilies([u"Franklin Gothic Demi Cond"])
        font4.setPointSize(9)
        font4.setStyleStrategy(QFont.PreferAntialias)
        self.frame_11.setFont(font4)
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Plain)
        self.verticalLayout_7 = QVBoxLayout(self.frame_11)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.selected_label = QLabel(self.frame_11)
        self.selected_label.setObjectName(u"selected_label")

        self.verticalLayout_7.addWidget(self.selected_label)

        self.res_set_label = QLabel(self.frame_11)
        self.res_set_label.setObjectName(u"res_set_label")

        self.verticalLayout_7.addWidget(self.res_set_label)


        self.verticalLayout_5.addWidget(self.frame_11)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.set_res_group = QGroupBox(self.frame_6)
        self.set_res_group.setObjectName(u"set_res_group")
        self.set_res_group.setFont(font1)
        self.verticalLayout_3 = QVBoxLayout(self.set_res_group)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.res_512_btn = QPushButton(self.set_res_group)
        self.res_512_btn.setObjectName(u"res_512_btn")
        self.res_512_btn.setFont(font1)

        self.gridLayout.addWidget(self.res_512_btn, 1, 0, 1, 1)

        self.res_1024_btn = QPushButton(self.set_res_group)
        self.res_1024_btn.setObjectName(u"res_1024_btn")
        self.res_1024_btn.setFont(font1)

        self.gridLayout.addWidget(self.res_1024_btn, 1, 1, 1, 1)

        self.res_quater_btn = QPushButton(self.set_res_group)
        self.res_quater_btn.setObjectName(u"res_quater_btn")
        self.res_quater_btn.setFont(font1)

        self.gridLayout.addWidget(self.res_quater_btn, 3, 1, 1, 1)

        self.res_2048_btn = QPushButton(self.set_res_group)
        self.res_2048_btn.setObjectName(u"res_2048_btn")
        self.res_2048_btn.setFont(font1)

        self.gridLayout.addWidget(self.res_2048_btn, 2, 0, 1, 1)

        self.res_4096_btn = QPushButton(self.set_res_group)
        self.res_4096_btn.setObjectName(u"res_4096_btn")
        self.res_4096_btn.setFont(font1)

        self.gridLayout.addWidget(self.res_4096_btn, 2, 1, 1, 1)

        self.res_half_btn = QPushButton(self.set_res_group)
        self.res_half_btn.setObjectName(u"res_half_btn")
        self.res_half_btn.setFont(font1)

        self.gridLayout.addWidget(self.res_half_btn, 3, 0, 1, 1)

        self.res_128_btn = QPushButton(self.set_res_group)
        self.res_128_btn.setObjectName(u"res_128_btn")
        self.res_128_btn.setFont(font1)

        self.gridLayout.addWidget(self.res_128_btn, 0, 0, 1, 1)

        self.res_256_btn = QPushButton(self.set_res_group)
        self.res_256_btn.setObjectName(u"res_256_btn")
        self.res_256_btn.setFont(font1)

        self.gridLayout.addWidget(self.res_256_btn, 0, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.frame_8 = QFrame(self.set_res_group)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy5)
        self.frame_8.setFont(font1)
        self.frame_8.setLineWidth(0)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, -1, 0, -1)
        self.size_res_entry = QLineEdit(self.frame_8)
        self.size_res_entry.setObjectName(u"size_res_entry")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.size_res_entry.sizePolicy().hasHeightForWidth())
        self.size_res_entry.setSizePolicy(sizePolicy6)
        self.size_res_entry.setMinimumSize(QSize(40, 0))
        self.size_res_entry.setMaximumSize(QSize(50, 16777215))
        self.size_res_entry.setFont(font1)
        self.size_res_entry.setMaxLength(5)
        self.size_res_entry.setAlignment(Qt.AlignCenter)
        self.size_res_entry.setClearButtonEnabled(False)

        self.horizontalLayout_6.addWidget(self.size_res_entry)

        self.set_res_btn = QPushButton(self.frame_8)
        self.set_res_btn.setObjectName(u"set_res_btn")
        self.set_res_btn.setFont(font)

        self.horizontalLayout_6.addWidget(self.set_res_btn)


        self.verticalLayout_3.addWidget(self.frame_8)


        self.verticalLayout_2.addWidget(self.set_res_group)


        self.horizontalLayout_3.addWidget(self.frame_6)


        self.verticalLayout.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setAutoFillBackground(True)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(10, 0, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.progressBar = QProgressBar(self.frame_5)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(400, 0))
        self.progressBar.setFont(font)
        self.progressBar.setValue(60)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setTextVisible(True)

        self.horizontalLayout_4.addWidget(self.progressBar)

        self.frame_10 = QFrame(self.frame_5)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.overwrite_btn = QRadioButton(self.frame_10)
        self.overwrite_btn.setObjectName(u"overwrite_btn")
        self.overwrite_btn.setFont(font)

        self.horizontalLayout_8.addWidget(self.overwrite_btn)

        self.rename_old_btn = QRadioButton(self.frame_10)
        self.rename_old_btn.setObjectName(u"rename_old_btn")
        self.rename_old_btn.setFont(font)
        self.rename_old_btn.setChecked(True)

        self.horizontalLayout_8.addWidget(self.rename_old_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 0, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.execute_btn = QPushButton(self.frame_10)
        self.execute_btn.setObjectName(u"execute_btn")
        self.execute_btn.setMinimumSize(QSize(220, 0))
        font5 = QFont()
        font5.setPointSize(12)
        font5.setStyleStrategy(QFont.PreferAntialias)
        self.execute_btn.setFont(font5)
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/shrink 213.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.execute_btn.setIcon(icon3)
        self.execute_btn.setIconSize(QSize(60, 16))

        self.horizontalLayout_8.addWidget(self.execute_btn)


        self.horizontalLayout_4.addWidget(self.frame_10)


        self.verticalLayout.addWidget(self.frame_5)


        self.horizontalLayout_7.addWidget(self.frame_2)


        self.verticalLayout_4.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.open_path_btn, self.open_file_btn)
        QWidget.setTabOrder(self.open_file_btn, self.select_all_btn)
        QWidget.setTabOrder(self.select_all_btn, self.select_none_btn)
        QWidget.setTabOrder(self.select_none_btn, self.size_thres_entry)
        QWidget.setTabOrder(self.size_thres_entry, self.set_thres_btn)
        QWidget.setTabOrder(self.set_thres_btn, self.size_res_entry)
        QWidget.setTabOrder(self.size_res_entry, self.set_res_btn)
        QWidget.setTabOrder(self.set_res_btn, self.overwrite_btn)
        QWidget.setTabOrder(self.overwrite_btn, self.rename_old_btn)
        QWidget.setTabOrder(self.rename_old_btn, self.execute_btn)
        QWidget.setTabOrder(self.execute_btn, self.res_128_btn)
        QWidget.setTabOrder(self.res_128_btn, self.res_256_btn)
        QWidget.setTabOrder(self.res_256_btn, self.res_512_btn)
        QWidget.setTabOrder(self.res_512_btn, self.res_1024_btn)
        QWidget.setTabOrder(self.res_1024_btn, self.res_2048_btn)
        QWidget.setTabOrder(self.res_2048_btn, self.res_4096_btn)
        QWidget.setTabOrder(self.res_4096_btn, self.res_half_btn)
        QWidget.setTabOrder(self.res_half_btn, self.res_quater_btn)
        QWidget.setTabOrder(self.res_quater_btn, self.path_label)
        QWidget.setTabOrder(self.path_label, self.restart_btn)
        QWidget.setTabOrder(self.restart_btn, self.tableWidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Texture Scaler", None))
        MainWindow.setProperty("frameShape", QCoreApplication.translate("MainWindow", u"NoFrame", None))
        self.restart_btn.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
        self.path_label.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Choose Directory or Textures from Disk", None))
        self.open_path_btn.setText(QCoreApplication.translate("MainWindow", u"Open Folder", None))
        self.open_file_btn.setText(QCoreApplication.translate("MainWindow", u"Open Images", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u221a", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Original", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Scaled", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Tiled", None));
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Select", None))
        self.select_all_btn.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.select_none_btn.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.size_thres_entry.setText("")
        self.size_thres_entry.setPlaceholderText(QCoreApplication.translate("MainWindow", u"2048", None))
        self.set_thres_btn.setText(QCoreApplication.translate("MainWindow", u"By Threshold", None))
        self.selected_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.res_set_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.set_res_group.setTitle(QCoreApplication.translate("MainWindow", u"Set Resolution", None))
        self.res_512_btn.setText(QCoreApplication.translate("MainWindow", u"512", None))
        self.res_1024_btn.setText(QCoreApplication.translate("MainWindow", u"1024", None))
        self.res_quater_btn.setText(QCoreApplication.translate("MainWindow", u"Quater", None))
        self.res_2048_btn.setText(QCoreApplication.translate("MainWindow", u"2048", None))
        self.res_4096_btn.setText(QCoreApplication.translate("MainWindow", u"4096", None))
        self.res_half_btn.setText(QCoreApplication.translate("MainWindow", u"Half", None))
        self.res_128_btn.setText(QCoreApplication.translate("MainWindow", u"128", None))
        self.res_256_btn.setText(QCoreApplication.translate("MainWindow", u"256", None))
        self.size_res_entry.setPlaceholderText(QCoreApplication.translate("MainWindow", u"1024", None))
        self.set_res_btn.setText(QCoreApplication.translate("MainWindow", u"Set Resolution", None))
        self.overwrite_btn.setText(QCoreApplication.translate("MainWindow", u"Overwrite Existing Texture", None))
        self.rename_old_btn.setText(QCoreApplication.translate("MainWindow", u"Create Backup Folder", None))
        self.execute_btn.setText(QCoreApplication.translate("MainWindow", u"Execute", None))
    # retranslateUi

