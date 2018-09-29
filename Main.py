import sys, csv

from PyQt5 import QtCore, QtGui, QtWidgets
from FileSelectPopUp import FileSelect
 
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		
		# Start the main window
		self.initUI()
		
		# Open the file import popup
		self.dialog = FileSelect()
		self.dialog.setupUi(self.dialog)
		self.dialog.gotFileName.connect(self.importFile)
		self.dialog.exec_() 
		
	def initUI(self):
		self.setWindowState(QtCore.Qt.WindowMaximized)
		self.setWindowTitle('BOM Creator')
		central_widget = QtWidgets.QWidget(self)
		self.setCentralWidget(central_widget)
		
		stdicon = self.style().standardIcon
		style = QtWidgets.QStyle
		
		# New file button toolbar
		newFileButton = QtWidgets.QAction(stdicon(style.SP_FileIcon), 'New File', self)
		newFileButton.setShortcut('Ctrl+N')
		newFileButton.setStatusTip('New File')
		newFileButton.triggered.connect(self.newFile)
		
		# Open button toolbar
		openButton = QtWidgets.QAction(stdicon(style.SP_DialogOpenButton), 'Open', self)
		openButton.setShortcut('Ctrl+O')
		openButton.setStatusTip('Open CSV File')
		openButton.triggered.connect(self.openCSV)
		
		# Import button toolbar
		importButton = QtWidgets.QAction(stdicon(style.SP_DialogOkButton), 'Import', self)
		importButton.setShortcut('Ctrl+I')
		importButton.setStatusTip('Import Kicad PCB File')
		importButton.triggered.connect(self.openFileNamesDialog)
		
		# Save button toolbar
		saveButton = QtWidgets.QAction(stdicon(style.SP_DialogSaveButton), 'Save', self)
		saveButton.setShortcut('Ctrl+S')
		saveButton.setStatusTip('Save File')
		saveButton.triggered.connect(self.saveCSV)
		
		# Exit button toolbar
		exitAction = QtWidgets.QAction(stdicon(style.SP_BrowserStop),'Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit')
		exitAction.triggered.connect(self.closeEvent)
		
		# Add the buttons to the toolbar
		self.toolbar = self.addToolBar('Tool Bar')
		self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		self.toolbar.addAction(newFileButton)
		self.toolbar.addAction(openButton)
		self.toolbar.addAction(saveButton)
		self.toolbar.addAction(importButton)
		self.toolbar.addAction(exitAction) 
		
		# Make the gride the central widget
		grid_layout = QtWidgets.QGridLayout(central_widget)
		central_widget.setLayout(grid_layout)
		
		# Make the table widget
		self.table = QtWidgets.QTableWidget(self)
		self.table.setColumnCount(26)
		self.table.setRowCount(100)
		self.table.horizontalHeader().setDefaultSectionSize(100)

		grid_layout.addWidget(self.table, 0, 0)   # Adding the table to the grid
		
		self.show()
		
	def openFileNamesDialog(self):    
		options = QtWidgets.QFileDialog.Options()
		fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Select File',
		'', 'kicad_pcb files (*.kicad_pcb);;All Files (*)', options=options)
		if fileName:
			self.importFile(fileName)
		
	def importFile(self, filename):
		with open(filename, 'r') as imported:
			if imported:
				self.parseData(imported)
				self.setWindowTitle(filename + ' - BOM Manager')
			else:
				pass
	
	def parseData(self, parts):
		storage = {}
		sortedParts = {}
		#referenceList = []
		reference = None
		value = None
		
		# Get reference and vaules and add them to self.storage
		for line in parts:
			if 'fp_text reference' in line:
				reference = line.split(' ')[6]
			elif 'fp_text value' in line and '"' in line:
				value = line.split('"')[1]
			elif 'fp_text value' in line:
				value = line.split(' ')[6]

			if reference != None:
				storage[reference] = value
		
		# Sort the values and references			
		for reference, value in storage.items():
			if value not in sortedParts:
				referenceList = []
				referenceList.append(reference)
				sortedParts[value] = referenceList
			else:
				sortedParts[value].append(reference)
				
		# Add Column titles
		self.table.setItem(0, 0, QtWidgets.QTableWidgetItem('Quanity'))
		self.table.setItem(0, 1, QtWidgets.QTableWidgetItem('Reference'))
		self.table.setItem(0, 2, QtWidgets.QTableWidgetItem('Value'))
		self.table.setItem(0, 3, QtWidgets.QTableWidgetItem('Description'))
		self.table.setItem(0, 4, QtWidgets.QTableWidgetItem('Manufacurer and Part #'))
		self.table.setItem(0, 5, QtWidgets.QTableWidgetItem('Suplier and Part #'))
		
		# Add the data to the tables
		count = 1
		for value, reference in sorted(sortedParts.items()):
			partCount = len(sortedParts[value])
			stringReference = ', '.join(reference)
			self.table.insertRow(count)
			self.table.setItem(count, 0, QtWidgets.QTableWidgetItem(str(partCount)))
			self.table.setItem(count, 1, QtWidgets.QTableWidgetItem(stringReference))
			self.table.setItem(count, 2, QtWidgets.QTableWidgetItem(value))
			count += 1
		self.table.resizeColumnsToContents()

	def saveCSV(self):
		fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV(*.csv)')
		if fileName != '':
			with open(str(fileName), 'w', newline='') as stream:
				writer = csv.writer(stream)
				for row in range(self.table.rowCount()):
					rowdata = []
					for column in range(self.table.columnCount()):
						item = self.table.item(row, column)
						if item is None:
							pass
						else:
							rowdata.append(item.text())
					writer.writerow(rowdata)
				
	def openCSV(self):
		rowCount = 0
		columnCount = 0
		fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV(*.csv)')
		if fileName != '':
			with open(str(fileName), 'r') as stream:
				self.table.setRowCount(1)
				for rowdata in csv.reader(stream):
					self.table.insertRow(rowCount)
					for column in rowdata:
						self.table.setItem(rowCount, columnCount, QtWidgets.QTableWidgetItem(column))
						columnCount += 1
					columnCount = 0
					rowCount += 1
		self.table.resizeColumnsToContents()

	def newFile(self):
		self.saveBeforeContin()
		self.table.horizontalHeader().setDefaultSectionSize(100)
		self.table.clear()
	
	
	# Save before continue popup
	def saveBeforeContin(self):
		reply = QtWidgets.QMessageBox.question(
		self, 'Message',
		'Are you sure you want to continue? Any unsaved work will be lost.',
		QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Cancel,
		QtWidgets.QMessageBox.Save)

		if reply == QtWidgets.QMessageBox.Close:
			pass
		if reply == QtWidgets.QMessageBox.Save:
			self.saveCSV()
	
	# Save before close popup
	def closeEvent(self, event):
		reply = QtWidgets.QMessageBox.question(
		self, 'Message',
		'Are you sure you want to quit? Any unsaved work will be lost.',
		QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Cancel,
		QtWidgets.QMessageBox.Save)

		if reply == QtWidgets.QMessageBox.Close:
			QtWidgets.qApp.quit()
		if reply == QtWidgets.QMessageBox.Save:
			self.saveCSV()
		else:
			event.ignore()
            

if __name__ == '__main__':
 
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    mw = MainWindow()
    sys.exit(app.exec())
