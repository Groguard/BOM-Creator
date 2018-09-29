# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog
from PyQt5.QtGui import QIcon

class FileSelect(QDialog):
	
	gotFileName = QtCore.pyqtSignal(str)
	
	def __init__(self):
		super(FileSelect, self).__init__()
	
	def setupUi(self, Dialog):
		Dialog.setObjectName("File Select")
		Dialog.resize(401, 202)
		self.pushButton = QtWidgets.QPushButton(Dialog)
		self.pushButton.setGeometry(QtCore.QRect(10, 140, 381, 51))
		self.pushButton.setObjectName("pushButton")
		self.pushButton.clicked.connect(lambda:self.openFileNamesDialog())
		self.label = QtWidgets.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(0, 20, 401, 111))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(True)
		font.setWeight(75)
		self.label.setFont(font)
		self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setObjectName("label")

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("File Select", "File Select"))
		self.pushButton.setText(_translate("File Select", "Import"))
		self.label.setText(_translate("File Select", "Click Import and Select a Kicad_PCB file to begin"))

	def openFileNamesDialog(self):    
		options = QFileDialog.Options()
		#options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(None,"Select File", "","kicad_pcb files (*.kicad_pcb);;All Files (*)", options=options)
		if fileName:
			self.gotFileName.emit(fileName)
		self.done(1)
