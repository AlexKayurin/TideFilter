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
        MainWindow.resize(800, 717)
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tideplot = PlotWidget(self.centralwidget)
        self.tideplot.setObjectName(u"tideplot")

        self.horizontalLayout_3.addWidget(self.tideplot)

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

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

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

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

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

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setEnabled(False)
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.groupBox_2.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.rb_RejectTime = QRadioButton(self.groupBox_2)
        self.rb_RejectTime.setObjectName(u"rb_RejectTime")
        self.rb_RejectTime.setChecked(True)

        self.verticalLayout_5.addWidget(self.rb_RejectTime)

        self.rb_RejectPoint = QRadioButton(self.groupBox_2)
        self.rb_RejectPoint.setObjectName(u"rb_RejectPoint")

        self.verticalLayout_5.addWidget(self.rb_RejectPoint)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
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
        self.l_text.setMinimumSize(QSize(150, 20))
        self.l_text.setMaximumSize(QSize(150, 20))
        font = QFont()
        font.setBold(True)
        self.l_text.setFont(font)
        self.l_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        self.ltide = QLabel(self.centralwidget)
        self.ltide.setObjectName(u"ltide")
        self.ltide.setMinimumSize(QSize(150, 20))
        self.ltide.setMaximumSize(QSize(150, 20))

        self.horizontalLayout.addWidget(self.ltide)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

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

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Gaussian Tide Filter", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load file(s)", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
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
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Rejection mode", None))
        self.rb_RejectTime.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.rb_RejectPoint.setText(QCoreApplication.translate("MainWindow", u"Point", None))
        self.b_reject.setText(QCoreApplication.translate("MainWindow", u"Reject", None))
        self.b_run.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.b_export.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.l_text.setText(QCoreApplication.translate("MainWindow", u"Press DEL to reject", None))
        self.l4.setText(QCoreApplication.translate("MainWindow", u"Time:", None))
        self.ltime.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.l5.setText(QCoreApplication.translate("MainWindow", u"Tide:", None))
        self.ltide.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.l_filename.setText(QCoreApplication.translate("MainWindow", u"Time span", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

