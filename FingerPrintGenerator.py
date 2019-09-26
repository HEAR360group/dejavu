# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton
from dejavu import Dejavu
import dejavu.shared
import subprocess
import shlex
import dejavu.fingerprint

class MyThread(QtCore.QThread):
    updated = QtCore.pyqtSignal(str)

    def run( self ):
        dejavu.shared.UITEXTLOGGER = self.updated;
        dejavu.shared.DATABASE_FILE = self.outputFilePath  

#        self.updated.emit("Converting " + self.inputFilePath + " to 16bit 3 channels PCM")
#        cmd = shlex.split("./ffmpeg -i " + self.inputFilePath + " -af \"pan=2.1|c0=c0|c1=c1|c2=c2\" temp.wav -y")
##        command = "-i " + self.inputFilePath + " -af \"pan=2.1c0|c1=c1|c2=c2\" temp.wav"
#        try:
#            subprocess.check_output(cmd)
#        except subprocess.CalledProcessError as e:
#            self.updated.emit("Error, " + e.output)
#            self.pushButton.setEnabled(True)
#            return
#            
#        self.updated.emit("Finished converting format for " + self.inputFilePath) 
        
#        # do some functionality
        djv = Dejavu({})
#        djv.uitextappend = self.updated
        #clear DB
        djv.empty_db()
        
        djv.fingerprint_file(self.inputFilePath)
        
        self.pushButton.setEnabled(True)
        self.spinBox.setEnabled(True)
#        for i in range(100):
#        self.updated.emit(self.inputFilePath)

class Ui_Form(object):
    def updateText( self, text ):
        self.plainTextEdit.appendPlainText(text);
        if "Converting " in text:
            self.progressBar.setValue(0)
        elif "Finished converting format for " in text:
            self.progressBar.setValue(20)
        elif "Finished channel 1/3 for" in text:
            self.progressBar.setValue(40)
        elif "Finished channel 2/3 for" in text:
            self.progressBar.setValue(60)  
        elif "Finished channel 3/3 for" in text:
            self.progressBar.setValue(80)
        elif "Finished saving finger prints to Database for" in text:
            self.progressBar.setValue(100)
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.form,"Select an audio file", "","Audio Files (*.wav)", options=options)
        if fileName:
            print(fileName)
            self.inputFilePath = fileName 
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(True)
            
            
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self.form,"Select the path for saving the SQLite database of finger prints","newDB.db","SQLite Files (*.db)", options=options)
        if fileName:
            print(fileName)
            self.pushButton_2.setEnabled(False)
            self.spinBox.setEnabled(False)
            self._thread = MyThread(Form)
            self._thread.inputFilePath = self.inputFilePath
            self._thread.outputFilePath = fileName
            self._thread.pushButton = self.pushButton
            self._thread.pushButton_2 = self.pushButton_2
            self._thread.spinBox = self.spinBox
            self._thread.updated.connect(self.updateText)
            self._thread.start()
            
    def button_pressed(self):
        self.openFileNameDialog()
        
    def button2_pressed(self):
        self.saveFileDialog()
        
    def spinBox_valueChanged(self):
        dejavu.fingerprint.PEAK_NEIGHBORHOOD_SIZE = self.spinBox.value()
        
    def setupUi(self, Form):
        Form.setObjectName("Finger Prints Generator")
        Form.resize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setAutoFillBackground(False)
        self.spinBox.setMinimum(10)
        self.spinBox.setMaximum(50)
        self.spinBox.setProperty("value", 20)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        self.form = Form
        self.spinBox.valueChanged.connect(self.spinBox_valueChanged)
        self.pushButton.clicked.connect(self.button_pressed)
        self.pushButton_2.clicked.connect(self.button2_pressed)
        self.pushButton_2.setEnabled(False)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Hear360 Finger Print Generator"))
        self.label.setText(_translate("Form", "PEAK NEIGHBORHOOD SIZE:"))
        self.pushButton.setText(_translate("Form", "Step1: Select a PCM audio file (16bit) to generate finger prints"))
        self.pushButton_2.setText(_translate("Form", "Step 2: Select the path for saving the SQLite database of finger prints"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

