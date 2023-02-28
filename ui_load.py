# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'load.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(514, 365)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_6.addWidget(self.label_2)

        self.doubleSpinBox = QDoubleSpinBox(Form)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")

        self.horizontalLayout_6.addWidget(self.doubleSpinBox)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.doubleSpinBox_2 = QDoubleSpinBox(Form)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.doubleSpinBox_3 = QDoubleSpinBox(Form)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")

        self.horizontalLayout_3.addWidget(self.doubleSpinBox_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.doubleSpinBox_4 = QDoubleSpinBox(Form)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        self.doubleSpinBox_4.setValue(30.000000000000000)

        self.horizontalLayout_2.addWidget(self.doubleSpinBox_4)

        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_2.addWidget(self.label_8)

        self.comboBox_2 = QComboBox(Form)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_2.addWidget(self.comboBox_2)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_2.addWidget(self.label_7)

        self.comboBox = QComboBox(Form)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_2.addWidget(self.comboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.spinBox = QSpinBox(Form)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout_4.addWidget(self.spinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_7.addWidget(self.label_9)

        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_7.addWidget(self.lineEdit_2)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_5.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_5.addWidget(self.pushButton_3)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u5bfc\u5165\u8f68\u8ff9\u6570\u636e\u4e0e\u8bbe\u8ba1\u4fe1\u606f", None))
        self.lineEdit.setText("")
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8d77\u59cb\u70b9\u4f4d\u7f6e\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5317\u5750\u6807\uff08m\uff09", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u4e1c\u5750\u6807\uff08m\uff09", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u65b9\u4f4d\u6539\u53d8\u91cf\uff08\u00b0\uff09\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u72d7\u817f\u89d2\u8ba1\u7b97\u95f4\u9694\uff08m\uff09\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u4e95\u7c7b\u578b\uff1a", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Form", u"\u9646\u5730", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Form", u"\u6d77\u4e0a", None))

        self.label_7.setText(QCoreApplication.translate("Form", u"\u5355\u4f4d", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"\u7c73\u5236", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"\u82f1\u5236", None))

        self.label_5.setText(QCoreApplication.translate("Form", u"\u63d2\u503c\u70b9\u4e2a\u6570\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u4e95\u540d\uff1a", None))
        self.lineEdit_2.setText("")
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

