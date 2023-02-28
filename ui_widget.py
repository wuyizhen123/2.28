# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.load_wellprofile = QAction(MainWindow)
        self.load_wellprofile.setObjectName(u"load_wellprofile")
        self.plot_well_profile = QAction(MainWindow)
        self.plot_well_profile.setObjectName(u"plot_well_profile")
        self.well_numbers = QAction(MainWindow)
        self.well_numbers.setObjectName(u"well_numbers")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.well_numbers)
        self.menu.addAction(self.load_wellprofile)
        self.menu.addSeparator()
        self.menu_2.addAction(self.plot_well_profile)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4e09\u7ef4\u4e95\u7b52\u6a21\u578b\u4e0e\u98ce\u9669\u4e95\u6bb5\u8bc6\u522b", None))
        self.load_wellprofile.setText(QCoreApplication.translate("MainWindow", u"\u4e95\u659c\u53c2\u6570", None))
        self.plot_well_profile.setText(QCoreApplication.translate("MainWindow", u"\u4e09\u7ef4\u4e95\u773c\u8f68\u8ff9\u56fe", None))
        self.well_numbers.setText(QCoreApplication.translate("MainWindow", u"\u4e95\u6570", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u8f93\u5165", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u7ed8\u56fe", None))
    # retranslateUi

