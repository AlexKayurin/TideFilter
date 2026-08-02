# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_UI_Config.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 200)
        MainWindow.setMinimumSize(QSize(700, 200))
        MainWindow.setMaximumSize(QSize(700, 200))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(75, 20))
        self.label.setMaximumSize(QSize(75, 20))

        self.horizontalLayout.addWidget(self.label)

        self.le_file_format = QLineEdit(self.centralwidget)
        self.le_file_format.setObjectName(u"le_file_format")
        self.le_file_format.setMinimumSize(QSize(0, 25))
        self.le_file_format.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.le_file_format)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(75, 20))
        self.label_2.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.le_date_format = QLineEdit(self.centralwidget)
        self.le_date_format.setObjectName(u"le_date_format")
        self.le_date_format.setMinimumSize(QSize(0, 25))
        self.le_date_format.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_2.addWidget(self.le_date_format)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(75, 20))
        self.label_3.setMaximumSize(QSize(75, 20))

        self.horizontalLayout_3.addWidget(self.label_3)

        self.le_time_format = QLineEdit(self.centralwidget)
        self.le_time_format.setObjectName(u"le_time_format")
        self.le_time_format.setMinimumSize(QSize(0, 25))
        self.le_time_format.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_3.addWidget(self.le_time_format)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.b_ok = QPushButton(self.centralwidget)
        self.b_ok.setObjectName(u"b_ok")
        self.b_ok.setMinimumSize(QSize(75, 40))
        self.b_ok.setMaximumSize(QSize(75, 40))

        self.horizontalLayout_4.addWidget(self.b_ok)

        self.b_cancel = QPushButton(self.centralwidget)
        self.b_cancel.setObjectName(u"b_cancel")
        self.b_cancel.setMinimumSize(QSize(75, 40))
        self.b_cancel.setMaximumSize(QSize(75, 40))

        self.horizontalLayout_4.addWidget(self.b_cancel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"File format", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Date format", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Time format", None))
        self.b_ok.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.b_cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
    # retranslateUi

