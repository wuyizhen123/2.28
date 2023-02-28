# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(233, 374)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBox = QComboBox(Form)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.comboBox_2 = QComboBox(Form)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_2.addWidget(self.comboBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.comboBox_3 = QComboBox(Form)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.horizontalLayout_3.addWidget(self.comboBox_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.spinBox = QSpinBox(Form)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setValue(2)

        self.horizontalLayout_4.addWidget(self.spinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_5.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_5.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u4f5c\u56fe\u4fe1\u606f\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u4f5c\u56fe\u7c7b\u578b\uff1a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"3d", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"top", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"vs", None))

        self.label_2.setText(QCoreApplication.translate("Form", u"\u6df1\u8272\uff1a", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Form", u"\u5426", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Form", u"\u662f", None))

        self.label_3.setText(QCoreApplication.translate("Form", u"\u989c\u8272\u533a\u5206\u7c7b\u578b\uff1a", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("Form", u"\u65e0", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Form", u"dls", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("Form", u"dl", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("Form", u"tvd", None))
        self.comboBox_3.setItemText(4, QCoreApplication.translate("Form", u"md", None))
        self.comboBox_3.setItemText(5, QCoreApplication.translate("Form", u"inc", None))
        self.comboBox_3.setItemText(6, QCoreApplication.translate("Form", u"azi", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"\u56fe\u5f62\u5c3a\u5bf8\uff1a", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

