# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'combinator.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CombinatorForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAdd = QtWidgets.QPushButton(Form)
        self.btnAdd.setCheckable(False)
        self.btnAdd.setObjectName("btnAdd")
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnUndo = QtWidgets.QPushButton(Form)
        self.btnUndo.setObjectName("btnUndo")
        self.horizontalLayout.addWidget(self.btnUndo)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.btnCombine = QtWidgets.QPushButton(Form)
        self.btnCombine.setObjectName("btnCombine")
        self.verticalLayout_2.addWidget(self.btnCombine)
        self.lblInfo = QtWidgets.QPlainTextEdit(Form)
        self.lblInfo.setReadOnly(True)
        self.lblInfo.setObjectName("lblInfo")
        self.verticalLayout_2.addWidget(self.lblInfo)
        self.pbConvert = QtWidgets.QProgressBar(Form)
        self.pbConvert.setProperty("value", 0)
        self.pbConvert.setInvertedAppearance(False)
        self.pbConvert.setObjectName("pbConvert")
        self.verticalLayout_2.addWidget(self.pbConvert)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnAdd.setText(_translate("Form", "Add a SQLite Database file"))
        self.btnUndo.setText(_translate("Form", "Undo the last addition"))
        self.btnCombine.setText(_translate("Form", "Combine into \"fingerprint.db\""))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_CombinatorForm()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
