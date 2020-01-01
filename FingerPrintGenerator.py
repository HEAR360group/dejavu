# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton
from dejavu import Dejavu
from dejavu import Combinator
import dejavu.shared
import subprocess
import shlex
import dejavu.fingerprint

class GeneratorThread(QtCore.QThread):
    updated = QtCore.pyqtSignal(str)
    updatedWithPercentage = QtCore.pyqtSignal(str, int)

    def run( self ):
        dejavu.shared.UITEXTLOGGER = self.updated;
        dejavu.shared.DATABASE_FILE = self.outputFilePath

        lpf = self.spinBox_4.value()
        hpf = self.spinBox_5.value()

#        self.updated.emit("lpf:" + str(lpf) + ", hpf:" + str(hpf))

        af = ""

        if lpf != 0 or hpf != 0:
            af = "-af "
            if lpf != 0:
                af += ("lowpass=" + str(lpf) + ",lowpass=" + str(lpf) + ",lowpass=" + str(lpf) + ",lowpass=" + str(lpf))
            if hpf != 0:
                if lpf != 0:
                    af += ","
                af += ("highpass=" + str(hpf) + ",highpass=" + str(hpf) + ",highpass=" + str(hpf) + ",highpass=" + str(hpf))
            af += " "

        cmd48k = shlex.split("./ffmpeg -i " + self.inputFilePath.replace(" ", "\\ ") + " -ar 48000 " + af + "-c:a pcm_s16le temp48k.wav -y")
        cmd44k = shlex.split("./ffmpeg -i " + self.inputFilePath.replace(" ", "\\ ") + " -ar 44100 " + af + "-c:a pcm_s16le temp44k.wav -y")
        cmd16k = shlex.split("./ffmpeg -i " + self.inputFilePath.replace(" ", "\\ ") + " -ar 16000 " + af + "-c:a pcm_s16le temp16k.wav -y")
        cmd8k = shlex.split("./ffmpeg -i " + self.inputFilePath.replace(" ", "\\ ") + " -ar 8000 " + af + "-c:a pcm_s16le temp8k.wav -y")
#        cmd = shlex.split("./ffmpeg -i " + self.inputFilePath + " -af \"pan=2.1|c0=c0|c1=c1|c2=c2\" temp.wav -y")
#        command = "-i " + self.inputFilePath + " -af \"pan=2.1c0|c1=c1|c2=c2\" temp.wav"

#        self.updated.emit("./ffmpeg -i " + self.inputFilePath.replace(" ", "\\ ") + " -ar 8000 " + af + "-c:a pcm_s16le temp8k.wav -y")

#        # do some functionality
        djv = Dejavu({})
#        djv.uitextappend = self.updated
        #clear DB
        djv.empty_db()

        totalProcesses = 0
        if self.checkBox.isChecked():
            totalProcesses += 1
        if self.checkBox_2.isChecked():
            totalProcesses += 1
        if self.checkBox_3.isChecked():
            totalProcesses += 1
        if self.checkBox_4.isChecked():
            totalProcesses += 1

        totalProcessedPercentage = 0

        self.updatedWithPercentage.emit("Start converting " + self.inputFilePath, totalProcessedPercentage)

        #48KHz
        if self.checkBox.isChecked():
            self.updated.emit("Converting " + self.inputFilePath + " to 48KHz 16bit PCM")

            try:
                subprocess.check_output(cmd48k)
            except subprocess.CalledProcessError as e:
                self.updated.emit("Error, " + e.output)
                self.pushButton.setEnabled(True)
                return

            totalProcessedPercentage += (50 / totalProcesses)
            self.updatedWithPercentage.emit("Finished converting 48KHz for " + self.inputFilePath, totalProcessedPercentage)

            djv.fingerprint_file("temp48k.wav")

            totalProcessedPercentage += (50 / totalProcesses)
            self.updatedWithPercentage.emit("Finished finger print generation for 48KHz for " + self.inputFilePath, totalProcessedPercentage)

        #44.1KHz
        if self.checkBox_2.isChecked():
            self.updated.emit("Converting " + self.inputFilePath + " to 44.1KHz 16bit PCM")

            try:
                subprocess.check_output(cmd44k)
            except subprocess.CalledProcessError as e:
                self.updated.emit("Error, " + e.output)
                self.pushButton.setEnabled(True)
                return

            totalProcessedPercentage += (50 / totalProcesses)
            self.updatedWithPercentage.emit("Finished converting 44.1KHz for " + self.inputFilePath, totalProcessedPercentage)

            djv.fingerprint_file("temp44k.wav")

            totalProcessedPercentage += (50 / totalProcesses)
            self.updatedWithPercentage.emit("Finished finger print generation for 44.1KHz for " + self.inputFilePath, totalProcessedPercentage)

        #16KHz
        if self.checkBox_3.isChecked():
            self.updated.emit("Converting " + self.inputFilePath + " to 16KHz 16bit PCM")

            try:
                subprocess.check_output(cmd16k)
            except subprocess.CalledProcessError as e:
                self.updated.emit("Error, " + e.output)
                self.pushButton.setEnabled(True)
                return

            totalProcessedPercentage += (50 / totalProcesses)
            self.updatedWithPercentage.emit("Finished converting 16KHz for " + self.inputFilePath, totalProcessedPercentage)

            djv.fingerprint_file("temp16k.wav")

            totalProcessedPercentage += (50 / totalProcesses)
            self.updatedWithPercentage.emit("Finished finger print generation for 16KHz for " + self.inputFilePath, totalProcessedPercentage)

        #8KHz
        if self.checkBox_4.isChecked():
            self.updated.emit("Converting " + self.inputFilePath + " to 8KHz 16bit PCM")

            try:
                subprocess.check_output(cmd8k)
            except subprocess.CalledProcessError as e:
                self.updated.emit("Error, " + e.output)
                self.pushButton.setEnabled(True)
                return

            totalProcessedPercentage += (50 / totalProcesses)
            self.updatedWithPercentage.emit("Finished converting 8KHz for " + self.inputFilePath, totalProcessedPercentage)

            djv.fingerprint_file("temp8k.wav")

            totalProcessedPercentage += (50 / totalProcesses)
            self.updatedWithPercentage.emit("Finished finger print generation for 8KHz for " + self.inputFilePath, totalProcessedPercentage)

        totalProcessedPercentage = 100
        self.updatedWithPercentage.emit("Finished finger prints generation for " + self.inputFilePath, totalProcessedPercentage)


        self.pushButton.setEnabled(True)
#        self.spinBox.setEnabled(True)
#        for i in range(100):
#        self.updated.emit(self.inputFilePath)

class GeneratorWindow(QtWidgets.QWidget):
    def updateText( self, text ):
        self.plainTextEdit.appendPlainText(text)

    def updatedTextWithPercentage( self, text, percentage ):
        self.plainTextEdit.appendPlainText(text)
        self.progressBar.setValue(percentage)

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
#            self.spinBox.setEnabled(False)
            self._thread = GeneratorThread()
            self._thread.inputFilePath = self.inputFilePath
            self._thread.outputFilePath = fileName
            self._thread.pushButton = self.pushButton
            self._thread.pushButton_2 = self.pushButton_2
            self._thread.spinBox = self.spinBox
            self._thread.checkBox = self.checkBox
            self._thread.checkBox_2 = self.checkBox_2
            self._thread.checkBox_3 = self.checkBox_3
            self._thread.checkBox_4 = self.checkBox_4
            self._thread.spinBox_4 = self.spinBox_4
            self._thread.spinBox_5 = self.spinBox_5
            self._thread.progressBar = self.progressBar
            self._thread.updated.connect(self.updateText)
            self._thread.updatedWithPercentage.connect(self.updatedTextWithPercentage)
            self._thread.start()

    def button_pressed(self):
        self.openFileNameDialog()

    def button2_pressed(self):
        self.saveFileDialog()

    def spinBox_valueChanged(self):
        dejavu.fingerprint.PEAK_NEIGHBORHOOD_SIZE = self.spinBox.value()

    def spinBox_2_valueChanged(self):
        dejavu.fingerprint.DEFAULT_FAN_VALUE = self.spinBox_2.value()

    def spinBox_3_valueChanged(self):
        dejavu.fingerprint.DEFAULT_AMP_MIN = self.spinBox_3.value()

    def __init__(self):
        QtWidgets.QWidget.__init__(self) 
#        Form.setObjectName("Form")
        self.resize(600, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel()
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setAutoFillBackground(False)
        self.spinBox.setMinimum(10)
        self.spinBox.setMaximum(50)
        self.spinBox.setProperty("value", 20)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox()
        self.spinBox_2.setMinimum(5)
        self.spinBox_2.setMaximum(50)
        self.spinBox_2.setProperty("value", 15)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_3.addWidget(self.spinBox_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel()
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.spinBox_3 = QtWidgets.QSpinBox()
        self.spinBox_3.setProperty("value", 10)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout_4.addWidget(self.spinBox_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel()
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.spinBox_4 = QtWidgets.QSpinBox()
        self.spinBox_4.setMaximum(20000)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout_6.addWidget(self.spinBox_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_5 = QtWidgets.QLabel()
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_8.addWidget(self.label_5)
        self.spinBox_5 = QtWidgets.QSpinBox()
        self.spinBox_5.setMaximum(20000)
        self.spinBox_5.setObjectName("spinBox_5")
        self.horizontalLayout_8.addWidget(self.spinBox_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_4 = QtWidgets.QCheckBox()
        self.checkBox_4.setObjectName("checkBox_4")
        self.horizontalLayout_5.addWidget(self.checkBox_4)
        self.checkBox_3 = QtWidgets.QCheckBox()
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_5.addWidget(self.checkBox_3)
        self.checkBox_2 = QtWidgets.QCheckBox()
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_5.addWidget(self.checkBox_2)
        self.checkBox = QtWidgets.QCheckBox()
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_5.addWidget(self.checkBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton()
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.plainTextEdit = QtWidgets.QPlainTextEdit()
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(self)
#        QtCore.QMetaObject.connectSlotsByName(Form)
        
        self.setLayout(self.verticalLayout)

        self.form = self
        self.spinBox.valueChanged.connect(self.spinBox_valueChanged)
        self.spinBox_2.valueChanged.connect(self.spinBox_2_valueChanged)
        self.spinBox_3.valueChanged.connect(self.spinBox_3_valueChanged)
        self.pushButton.clicked.connect(self.button_pressed)
        self.pushButton_2.clicked.connect(self.button2_pressed)
        self.pushButton_2.setEnabled(False)
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SoundFi Finger Print Generator"))
        self.label.setText(_translate("Form", "PEAK_NEIGHBORHOOD_SIZE:"))
        self.label_2.setText(_translate("Form", "FAN_VALUE (degree of Finger Prints)"))
        self.label_3.setText(_translate("Form", "AMP_MIN (noise floor)"))
        self.label_4.setText(_translate("Form", "Low Pass Filter (Hz)"))
        self.label_5.setText(_translate("Form", "High Pass Filter (Hz)"))
        self.checkBox_4.setText(_translate("Form", "8KHz"))
        self.checkBox_3.setText(_translate("Form", "16KHz"))
        self.checkBox_2.setText(_translate("Form", "44.1KHz"))
        self.checkBox.setText(_translate("Form", "48KHz"))
        self.pushButton.setText(_translate("Form", "Step1: Select an audio file to generate finger prints"))
        self.pushButton_2.setText(_translate("Form", "Step 2: Select the path for saving the SQLite database of finger prints"))


class CombinatorThread(QtCore.QThread):
    updated = QtCore.pyqtSignal(str)
    updatedWithPercentage = QtCore.pyqtSignal(str, int)

    def run( self ):
        currentInputFileIndex = 0
        totalSteps = len(self.inputFilePaths) + 1
        for path in self.inputFilePaths:
            cmb = Combinator({})
            cmb.add_db(path)
            currentInputFileIndex = currentInputFileIndex + 1
            totalProcessedPercentage = currentInputFileIndex / totalSteps * 100
            self.updatedWithPercentage.emit("Completed combinating: " + self.inputFilePaths[currentInputFileIndex - 1], totalProcessedPercentage)
            
        cmb.save_db(self.outputFilePath)
        
        totalProcessedPercentage = 100
        self.updatedWithPercentage.emit("Fininshed, combined DB is saved at " + self.outputFilePath, totalProcessedPercentage)

        self.btnAdd.setEnabled(True)

class CombinatorWindow(QtWidgets.QWidget):
    def updateText( self, text ):
        self.lblInfo.appendPlainText(text)

    def updatedTextWithPercentage( self, text, percentage ):
        self.lblInfo.appendPlainText(text)
        self.pbConvert.setValue(percentage)
        
    def listToString(self, s):  
        # initialize an empty string 
        str1 = ""  
        
        # traverse in the string   
        for ele in s:  
            str1 += ele  
            str1 += "\n"
        
        # return string   
        return str1[:-1]
        
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Step1: Select SQLite DB files", "","Database Files (*.db)", options=options)
        if fileNames:
            fuck = self.listToString(fileNames)
            self.updateText("Selected SQLite DataBase Files:\n" + fuck)
            self.inputFilePaths = [];
            self.inputFilePaths.extend(fileNames)
            self.btnAdd.setEnabled(False)
            self.btnCombine.setEnabled(True)
            
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Step2: Select the path for exported SQLite database file","fingerprint.db","SQLite Files (*.db)", options=options)
        if fileName:
            print(fileName)
            self.btnCombine.setEnabled(False)
            self._thread = CombinatorThread()
            self._thread.inputFilePaths = self.inputFilePaths
            self._thread.outputFilePath = fileName
            self._thread.btnAdd = self.btnAdd
            self._thread.lblInfo = self.lblInfo
            self._thread.pbConvert = self.pbConvert
            self._thread.updated.connect(self.updateText)
            self._thread.updatedWithPercentage.connect(self.updatedTextWithPercentage)
            self._thread.start()
    
    def btnAddPressed(self):
        self.openFileNameDialog()
    
    def btnCombinePressed(self):
        self.saveFileDialog()
        
        
    def __init__(self):
        QtWidgets.QWidget.__init__(self)       
 #       Form.setObjectName("CombinatorForm")
 #       Form.resize(600, 400)
        self.resize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAdd = QtWidgets.QPushButton()
        self.btnAdd.setCheckable(False)
        self.btnAdd.setObjectName("btnAdd")
        self.horizontalLayout.addWidget(self.btnAdd)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.btnCombine = QtWidgets.QPushButton()
        self.btnCombine.setObjectName("btnCombine")
        self.verticalLayout_2.addWidget(self.btnCombine)
        self.lblInfo = QtWidgets.QPlainTextEdit()
        self.lblInfo.setReadOnly(True)
        self.lblInfo.setObjectName("lblInfo")
        self.verticalLayout_2.addWidget(self.lblInfo)
        self.pbConvert = QtWidgets.QProgressBar()
        self.pbConvert.setProperty("value", 0)
        self.pbConvert.setInvertedAppearance(False)
        self.pbConvert.setObjectName("pbConvert")
        self.verticalLayout_2.addWidget(self.pbConvert)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(self)
#        QtCore.QMetaObject.connectSlotsByName(Form)
        
        self.setLayout(self.verticalLayout)
        
        self.btnAdd.clicked.connect(self.btnAddPressed)
        self.btnCombine.clicked.connect(self.btnCombinePressed)
        
        self.btnCombine.setEnabled(False)
        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SoundFi Finger Print Combinator"))
        self.btnAdd.setText(_translate("Form", "Add a SQLite Database file"))
        self.btnCombine.setText(_translate("Form", "Combine into \"fingerprint.db\""))

class MainWindow(QtWidgets.QWidget):
    def btnCombinerPressed(self):
        controller.show_combinator()
        
    def btnGeneratorPressed(self):
        controller.show_generator()
        
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
#        MainForm.setObjectName("MainForm")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnGenerator = QtWidgets.QPushButton()
        self.btnGenerator.setObjectName("btnGenerator")
        self.horizontalLayout.addWidget(self.btnGenerator)
        self.btnCombiner = QtWidgets.QPushButton()
        self.btnCombiner.setObjectName("btnCombiner")
        self.horizontalLayout.addWidget(self.btnCombiner)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(self)
#        QtCore.QMetaObject.connectSlotsByName(MainForm)
        
        self.setLayout(self.verticalLayout)
        
        self.btnCombiner.clicked.connect(self.btnCombinerPressed)
        self.btnGenerator.clicked.connect(self.btnGeneratorPressed)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "SoundFi FingerPrint Database ToolBox"))
        self.label.setText(_translate("MainForm", "SoundFi FingerPrint Database ToolBox"))
        self.btnGenerator.setText(_translate("MainForm", "Dababase Generator"))
        self.btnCombiner.setText(_translate("MainForm", "Database Combiner"))


class Controller:

    def __init__(self):
        pass

    def show_main(self):
        self.mainWindow = MainWindow()
#        self.mainWindow.switch_window.connect(self.show_main)
        self.mainWindow.show()

    def show_combinator(self):
        self.combinator = CombinatorWindow()
#        self.window.switch_window.connect(self.show_window_two)
        self.mainWindow.close()
        self.combinator.show()

    def show_generator(self):
        self.generator = GeneratorWindow()
        self.mainWindow.close()
        self.generator.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
#    MainForm = QtWidgets.QWidget()
#    mainwindow = MainWindow()
#    mainwindow.show()
#    combinatorWindow = CombinatorWindow()
#    combinatorWindow.show()
#    ui.setupUi(MainForm).show()
    sys.exit(app.exec_())
    
