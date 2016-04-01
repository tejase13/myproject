# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'results.ui'
#
# Created: Fri Apr  1 11:53:10 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sqlite3
import sys 

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

class Ui_Results(object):
    def setupUi(self, Results, query):
        Results.setObjectName(_fromUtf8("Results"))
        Results.setWindowModality(QtCore.Qt.ApplicationModal)
        Results.resize(400, 300)
        Results.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Results)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(Results)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setSortingEnabled(True)

        query += ';'
        print(query)
        conn = sqlite3.connect('be_proj_check.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall() 
        print (results)
        print(cursor.description)

        label = list()

        for item in cursor.description:
            label.append(item[0])
        print (label)


        self.tableWidget.setColumnCount(len(label))
        self.tableWidget.setRowCount(len(results))

        self.tableWidget.setHorizontalHeaderLabels(label)

        for i in range(len(results)):
            for j in range(len(label)):
                self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(str(results[i][j])))
        
        self.verticalLayout.addWidget(self.tableWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Results)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Results)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Results.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Results.reject)
        QtCore.QMetaObject.connectSlotsByName(Results)
        Results.show()
    

    def retranslateUi(self, Results):
        Results.setWindowTitle(_translate("Results", "Dialog", None))


'''
app = QtGui.QApplication([])
win = QtGui.QDialog()
foo = Ui_Results()
foo.setupUi(win)
sys.exit(app.exec_())
'''