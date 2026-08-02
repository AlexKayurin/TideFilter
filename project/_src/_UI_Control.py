# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_UI_Control.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 991)
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionEditconfig = QAction(MainWindow)
        self.actionEditconfig.setObjectName(u"actionEditconfig")
        self.actionShow_config = QAction(MainWindow)
        self.actionShow_config.setObjectName(u"actionShow_config")
        self.actionEdit_config = QAction(MainWindow)
        self.actionEdit_config.setObjectName(u"actionEdit_config")
        self.actionManual = QAction(MainWindow)
        self.actionManual.setObjectName(u"actionManual")
        self.actionLicense = QAction(MainWindow)
        self.actionLicense.setObjectName(u"actionLicense")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.dataplot = PlotWidget(self.centralwidget)
        self.dataplot.setObjectName(u"dataplot")

        self.horizontalLayout_3.addWidget(self.dataplot)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, -1, -1, -1)
        self.ch_showraw = QCheckBox(self.centralwidget)
        self.ch_showraw.setObjectName(u"ch_showraw")
        self.ch_showraw.setMinimumSize(QSize(150, 20))
        self.ch_showraw.setMaximumSize(QSize(150, 20))
        self.ch_showraw.setChecked(True)

        self.verticalLayout_2.addWidget(self.ch_showraw)

        self.line_1 = QFrame(self.centralwidget)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setFrameShape(QFrame.Shape.HLine)
        self.line_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.l6 = QLabel(self.centralwidget)
        self.l6.setObjectName(u"l6")
        self.l6.setMinimumSize(QSize(100, 20))
        self.l6.setMaximumSize(QSize(100, 20))

        self.horizontalLayout_4.addWidget(self.l6)

        self.sp_linestoskip = QSpinBox(self.centralwidget)
        self.sp_linestoskip.setObjectName(u"sp_linestoskip")
        self.sp_linestoskip.setMinimumSize(QSize(75, 20))
        self.sp_linestoskip.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_4.addWidget(self.sp_linestoskip)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.l3 = QLabel(self.centralwidget)
        self.l3.setObjectName(u"l3")
        self.l3.setMinimumSize(QSize(100, 20))
        self.l3.setMaximumSize(QSize(100, 20))

        self.horizontalLayout_9.addWidget(self.l3)

        self.sp_subsample = QSpinBox(self.centralwidget)
        self.sp_subsample.setObjectName(u"sp_subsample")
        self.sp_subsample.setMinimumSize(QSize(75, 20))
        self.sp_subsample.setMaximumSize(QSize(75, 20))
        self.sp_subsample.setMinimum(1)
        self.sp_subsample.setMaximum(10000)
        self.sp_subsample.setValue(10)

        self.horizontalLayout_9.addWidget(self.sp_subsample)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.l_filt_parameter = QLabel(self.centralwidget)
        self.l_filt_parameter.setObjectName(u"l_filt_parameter")
        self.l_filt_parameter.setMinimumSize(QSize(100, 20))
        self.l_filt_parameter.setMaximumSize(QSize(100, 20))

        self.horizontalLayout_6.addWidget(self.l_filt_parameter)

        self.le_filt_val = QLineEdit(self.centralwidget)
        self.le_filt_val.setObjectName(u"le_filt_val")
        self.le_filt_val.setMinimumSize(QSize(75, 20))
        self.le_filt_val.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_6.addWidget(self.le_filt_val)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.line_0 = QFrame(self.centralwidget)
        self.line_0.setObjectName(u"line_0")
        self.line_0.setFrameShape(QFrame.Shape.HLine)
        self.line_0.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_0)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.l7 = QLabel(self.centralwidget)
        self.l7.setObjectName(u"l7")
        self.l7.setMinimumSize(QSize(100, 20))
        self.l7.setMaximumSize(QSize(100, 20))

        self.horizontalLayout_5.addWidget(self.l7)

        self.le_zshift = QLineEdit(self.centralwidget)
        self.le_zshift.setObjectName(u"le_zshift")
        self.le_zshift.setMinimumSize(QSize(75, 20))
        self.le_zshift.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_5.addWidget(self.le_zshift)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.l8 = QLabel(self.centralwidget)
        self.l8.setObjectName(u"l8")
        self.l8.setMinimumSize(QSize(100, 20))
        self.l8.setMaximumSize(QSize(100, 20))

        self.horizontalLayout_7.addWidget(self.l8)

        self.le_tshift = QLineEdit(self.centralwidget)
        self.le_tshift.setObjectName(u"le_tshift")
        self.le_tshift.setMinimumSize(QSize(75, 20))
        self.le_tshift.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_7.addWidget(self.le_tshift)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 0))
        self.groupBox.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.rb_Gauss = QRadioButton(self.groupBox)
        self.rb_Gauss.setObjectName(u"rb_Gauss")
        self.rb_Gauss.setChecked(True)

        self.verticalLayout_4.addWidget(self.rb_Gauss)

        self.rb_FIR = QRadioButton(self.groupBox)
        self.rb_FIR.setObjectName(u"rb_FIR")

        self.verticalLayout_4.addWidget(self.rb_FIR)

        self.rb_Median = QRadioButton(self.groupBox)
        self.rb_Median.setObjectName(u"rb_Median")

        self.verticalLayout_4.addWidget(self.rb_Median)

        self.rb_Mean = QRadioButton(self.groupBox)
        self.rb_Mean.setObjectName(u"rb_Mean")

        self.verticalLayout_4.addWidget(self.rb_Mean)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.l10 = QLabel(self.centralwidget)
        self.l10.setObjectName(u"l10")
        self.l10.setMinimumSize(QSize(70, 20))
        self.l10.setMaximumSize(QSize(70, 20))
        self.l10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.l10)

        self.b_Yup = QPushButton(self.centralwidget)
        self.b_Yup.setObjectName(u"b_Yup")
        self.b_Yup.setMinimumSize(QSize(70, 70))
        self.b_Yup.setMaximumSize(QSize(70, 70))
        font = QFont()
        font.setPointSize(36)
        self.b_Yup.setFont(font)

        self.verticalLayout_6.addWidget(self.b_Yup)

        self.b_Yall = QPushButton(self.centralwidget)
        self.b_Yall.setObjectName(u"b_Yall")
        self.b_Yall.setMinimumSize(QSize(70, 70))
        self.b_Yall.setMaximumSize(QSize(70, 70))
        self.b_Yall.setFont(font)

        self.verticalLayout_6.addWidget(self.b_Yall)

        self.b_Ydown = QPushButton(self.centralwidget)
        self.b_Ydown.setObjectName(u"b_Ydown")
        self.b_Ydown.setMinimumSize(QSize(70, 70))
        self.b_Ydown.setMaximumSize(QSize(70, 70))
        self.b_Ydown.setFont(font)

        self.verticalLayout_6.addWidget(self.b_Ydown)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.b_augment = QPushButton(self.centralwidget)
        self.b_augment.setObjectName(u"b_augment")
        self.b_augment.setMinimumSize(QSize(100, 50))
        self.b_augment.setMaximumSize(QSize(100, 50))

        self.verticalLayout.addWidget(self.b_augment)

        self.b_align = QPushButton(self.centralwidget)
        self.b_align.setObjectName(u"b_align")
        self.b_align.setEnabled(False)
        self.b_align.setMinimumSize(QSize(100, 50))
        self.b_align.setMaximumSize(QSize(100, 50))

        self.verticalLayout.addWidget(self.b_align)

        self.b_reject = QPushButton(self.centralwidget)
        self.b_reject.setObjectName(u"b_reject")
        self.b_reject.setMinimumSize(QSize(100, 50))
        self.b_reject.setMaximumSize(QSize(100, 50))
        self.b_reject.setCheckable(True)
        self.b_reject.setChecked(False)

        self.verticalLayout.addWidget(self.b_reject)

        self.b_run = QPushButton(self.centralwidget)
        self.b_run.setObjectName(u"b_run")
        self.b_run.setMinimumSize(QSize(100, 50))
        self.b_run.setMaximumSize(QSize(100, 50))

        self.verticalLayout.addWidget(self.b_run)

        self.b_export = QPushButton(self.centralwidget)
        self.b_export.setObjectName(u"b_export")
        self.b_export.setMinimumSize(QSize(100, 50))
        self.b_export.setMaximumSize(QSize(100, 50))

        self.verticalLayout.addWidget(self.b_export)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalSpacer_3 = QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.l_text = QLabel(self.centralwidget)
        self.l_text.setObjectName(u"l_text")
        self.l_text.setMinimumSize(QSize(200, 110))
        self.l_text.setMaximumSize(QSize(200, 110))
        font1 = QFont()
        font1.setBold(True)
        self.l_text.setFont(font1)
        self.l_text.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_2.addWidget(self.l_text)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.l4 = QLabel(self.centralwidget)
        self.l4.setObjectName(u"l4")
        self.l4.setMinimumSize(QSize(75, 20))
        self.l4.setMaximumSize(QSize(75, 20))
        self.l4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.l4)

        self.ltime = QLabel(self.centralwidget)
        self.ltime.setObjectName(u"ltime")
        self.ltime.setMinimumSize(QSize(150, 20))
        self.ltime.setMaximumSize(QSize(150, 20))

        self.horizontalLayout.addWidget(self.ltime)

        self.l5 = QLabel(self.centralwidget)
        self.l5.setObjectName(u"l5")
        self.l5.setMinimumSize(QSize(75, 20))
        self.l5.setMaximumSize(QSize(75, 20))
        self.l5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.l5)

        self.ldata = QLabel(self.centralwidget)
        self.ldata.setObjectName(u"ldata")
        self.ldata.setMinimumSize(QSize(150, 20))
        self.ldata.setMaximumSize(QSize(150, 20))

        self.horizontalLayout.addWidget(self.ldata)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.l_filename = QLabel(self.centralwidget)
        self.l_filename.setObjectName(u"l_filename")
        self.l_filename.setMinimumSize(QSize(0, 20))
        self.l_filename.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_3.addWidget(self.l_filename)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionEdit_config)
        self.menuFile.addAction(self.actionShow_config)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionManual)
        self.menuFile.addAction(self.actionLicense)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"UniFilter", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load file(s)", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionEditconfig.setText(QCoreApplication.translate("MainWindow", u"Edit config", None))
        self.actionShow_config.setText(QCoreApplication.translate("MainWindow", u"Show config", None))
        self.actionEdit_config.setText(QCoreApplication.translate("MainWindow", u"Edit config", None))
        self.actionManual.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.actionLicense.setText(QCoreApplication.translate("MainWindow", u"License", None))
        self.ch_showraw.setText(QCoreApplication.translate("MainWindow", u"Show raw data", None))
        self.l6.setText(QCoreApplication.translate("MainWindow", u"Lines to skip", None))
        self.l3.setText(QCoreApplication.translate("MainWindow", u"Downsample", None))
        self.l_filt_parameter.setText(QCoreApplication.translate("MainWindow", u"Sigma", None))
        self.le_filt_val.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.l7.setText(QCoreApplication.translate("MainWindow", u"Apply Z shift (m)", None))
        self.le_zshift.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.l8.setText(QCoreApplication.translate("MainWindow", u"Apply T shift (s)", None))
        self.le_tshift.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.rb_Gauss.setText(QCoreApplication.translate("MainWindow", u"Gaussian", None))
        self.rb_FIR.setText(QCoreApplication.translate("MainWindow", u"FIR", None))
        self.rb_Median.setText(QCoreApplication.translate("MainWindow", u"Median", None))
        self.rb_Mean.setText(QCoreApplication.translate("MainWindow", u"Mean", None))
        self.l10.setText(QCoreApplication.translate("MainWindow", u"V Zoom", None))
        self.b_Yup.setText(QCoreApplication.translate("MainWindow", u"up", None))
        self.b_Yall.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.b_Ydown.setText(QCoreApplication.translate("MainWindow", u"down", None))
        self.b_augment.setText(QCoreApplication.translate("MainWindow", u"Augment", None))
        self.b_align.setText(QCoreApplication.translate("MainWindow", u"Align", None))
        self.b_reject.setText(QCoreApplication.translate("MainWindow", u"Reject/Accept", None))
        self.b_run.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.b_export.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.l_text.setText(QCoreApplication.translate("MainWindow", u"Press DEL to reject", None))
        self.l4.setText(QCoreApplication.translate("MainWindow", u"Time:", None))
        self.ltime.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.l5.setText(QCoreApplication.translate("MainWindow", u"Value:", None))
        self.ldata.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.l_filename.setText(QCoreApplication.translate("MainWindow", u"Time span", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

