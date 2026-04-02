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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tideplot = PlotWidget(self.centralwidget)
        self.tideplot.setObjectName(u"tideplot")

        self.horizontalLayout_2.addWidget(self.tideplot)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.l3 = QLabel(self.centralwidget)
        self.l3.setObjectName(u"l3")
        self.l3.setMinimumSize(QSize(75, 20))
        self.l3.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_9.addWidget(self.l3)

        self.sp_subsample = QSpinBox(self.centralwidget)
        self.sp_subsample.setObjectName(u"sp_subsample")
        self.sp_subsample.setMinimumSize(QSize(75, 20))
        self.sp_subsample.setMaximumSize(QSize(75, 20))
        self.sp_subsample.setMinimum(1)
        self.sp_subsample.setMaximum(10000)
        self.sp_subsample.setValue(10)

        self.horizontalLayout_9.addWidget(self.sp_subsample)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.l0 = QLabel(self.centralwidget)
        self.l0.setObjectName(u"l0")
        self.l0.setMinimumSize(QSize(75, 20))
        self.l0.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_6.addWidget(self.l0)

        self.le_sg_win = QLineEdit(self.centralwidget)
        self.le_sg_win.setObjectName(u"le_sg_win")
        self.le_sg_win.setMinimumSize(QSize(75, 20))
        self.le_sg_win.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_6.addWidget(self.le_sg_win)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.l1 = QLabel(self.centralwidget)
        self.l1.setObjectName(u"l1")
        self.l1.setMinimumSize(QSize(75, 20))
        self.l1.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_7.addWidget(self.l1)

        self.le_sg_ord = QLineEdit(self.centralwidget)
        self.le_sg_ord.setObjectName(u"le_sg_ord")
        self.le_sg_ord.setMinimumSize(QSize(75, 20))
        self.le_sg_ord.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_7.addWidget(self.le_sg_ord)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.l2 = QLabel(self.centralwidget)
        self.l2.setObjectName(u"l2")
        self.l2.setMinimumSize(QSize(75, 20))
        self.l2.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_8.addWidget(self.l2)

        self.le_ma_win = QLineEdit(self.centralwidget)
        self.le_ma_win.setObjectName(u"le_ma_win")
        self.le_ma_win.setMinimumSize(QSize(75, 20))
        self.le_ma_win.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_8.addWidget(self.le_ma_win)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

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

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

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


        self.verticalLayout_2.addLayout(self.horizontalLayout)

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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Tide Filter", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.l3.setText(QCoreApplication.translate("MainWindow", u"Downsample", None))
        self.l0.setText(QCoreApplication.translate("MainWindow", u"SG Window", None))
        self.le_sg_win.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.l1.setText(QCoreApplication.translate("MainWindow", u"SG Order", None))
        self.le_sg_ord.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.l2.setText(QCoreApplication.translate("MainWindow", u"MA Window", None))
        self.le_ma_win.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.b_run.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.b_export.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.l4.setText(QCoreApplication.translate("MainWindow", u"Time:", None))
        self.ltime.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.l5.setText(QCoreApplication.translate("MainWindow", u"Tide:", None))
        self.ltide.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

