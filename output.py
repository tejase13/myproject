# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prototype.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt4 import QtCore, QtGui
from nlpchecker import NLPChecker

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(824, 505)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.gridLayout.addLayout(self.verticalLayout_9, 3, 3, 1, 1)
        self.verticalLayout_10 = QtGui.QVBoxLayout()
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.execute_button = QtGui.QPushButton(self.centralwidget)
        self.execute_button.setEnabled(False)
        self.execute_button.setObjectName(_fromUtf8("execute_button"))
        self.verticalLayout_10.addWidget(self.execute_button)
        self.gridLayout.addLayout(self.verticalLayout_10, 3, 4, 1, 1)
        self.verticalLayout_11 = QtGui.QVBoxLayout()
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.gridLayout.addLayout(self.verticalLayout_11, 3, 5, 1, 1)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.gridLayout.addLayout(self.verticalLayout_8, 3, 2, 1, 1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.generated_query_label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(10)
        self.generated_query_label.setFont(font)
        self.generated_query_label.setScaledContents(True)
        self.generated_query_label.setObjectName(_fromUtf8("generated_query_label"))
        self.verticalLayout_7.addWidget(self.generated_query_label, QtCore.Qt.AlignHCenter)
        self.gridLayout.addLayout(self.verticalLayout_7, 2, 0, 1, 1)
        self.verticalLayout_12 = QtGui.QVBoxLayout()
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.gridLayout.addLayout(self.verticalLayout_12, 3, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.main_title = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(16)
        self.main_title.setFont(font)
        self.main_title.setObjectName(_fromUtf8("main_title"))
        self.verticalLayout_3.addWidget(self.main_title, QtCore.Qt.AlignHCenter)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 6)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.input_query_label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(10)
        self.input_query_label.setFont(font)
        self.input_query_label.setObjectName(_fromUtf8("input_query_label"))
        self.verticalLayout_4.addWidget(self.input_query_label, QtCore.Qt.AlignHCenter)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 0, 1, 1)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.input_query = QtGui.QLineEdit(self.centralwidget)
        self.input_query.setObjectName(_fromUtf8("input_query"))
        self.verticalLayout_5.addWidget(self.input_query)
        self.gridLayout.addLayout(self.verticalLayout_5, 1, 1, 1, 4)
        self.translate_button = QtGui.QPushButton(self.centralwidget)
        self.translate_button.setObjectName(_fromUtf8("translate_button"))
        self.gridLayout.addWidget(self.translate_button, 3, 1, 1, 1)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.generated_query = QtGui.QLabel(self.centralwidget)
        self.generated_query.setObjectName(_fromUtf8("generated_query"))
        self.verticalLayout_6.addWidget(self.generated_query)
        self.gridLayout.addLayout(self.verticalLayout_6, 2, 1, 1, 4)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 824, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.translate_button.clicked.connect(self.animateClick)
        MainWindow.show()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.execute_button.setText(_translate("MainWindow", "Execute", None))
        self.generated_query_label.setText(_translate("MainWindow", "Generated Query", None))
        self.main_title.setText(_translate("MainWindow", "Natural Language Query Processing", None))
        self.input_query_label.setText(_translate("MainWindow", "Input Query", None))
        self.translate_button.setText(_translate("MainWindow", "Translate", None))
        self.generated_query.setText(_translate("MainWindow", "", None))

    def animateClick(self):
        query = self.input_query.text()
        lp = NLPChecker()
        self.generated_query.setText(lp.execute(query))
        self.execute_button.setEnabled(True)

if __name__ == "__main__":
	app = QtGui.QApplication([])
	win = QtGui.QMainWindow()
	foo = Ui_MainWindow()
	foo.setupUi(win)
	sys.exit(app.exec_())
