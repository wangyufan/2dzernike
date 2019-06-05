
# coding=utf-8
import sys
from PyQt4 import QtGui, QtCore
import argparse
import crop
import peak_cluster



class MyDialog(QtGui.QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        self.gridlayout = QtGui.QGridLayout()
        self.label = QtGui.QLabel("start the task!")
        self.label1 = QtGui.QLabel("waiting for the processing...")
        # self.label2 = QtGui.QLabel("task finished!")
        self.cancalButton = QtGui.QPushButton("OK")
        self.gridlayout.addWidget(self.label, 0, 0)
        self.gridlayout.addWidget(self.label1, 1, 0)
        # self.gridlayout.addWidget(self.label2, 2, 0)
        self.gridlayout.addWidget(self.cancalButton, 3, 0)
        self.connect(self.cancalButton, QtCore.SIGNAL('clicked()'), self.OnCancel)
        self.setLayout(self.gridlayout)

    def OnCancel(self):
        self.done(0)

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Template generation...")
        self.cropTitle = QtGui.QLabel('')
        self.dataset = QtGui.QLabel('Input')
        self.datasetEdit = QtGui.QLineEdit()
        self.output = QtGui.QLabel('output')
        self.outputEdit = QtGui.QLineEdit()
        self.cropBrowse = QtGui.QPushButton("Browse")
        self.fileType = QtGui.QLabel('Frames used') 
        self.fileTypeEdit = QtGui.QLineEdit()  
        self.cropButton = QtGui.QPushButton("Crop peaks")
        self.cropResult = QtGui.QLineEdit()

        self.clusterTitle = QtGui.QLabel('')
        self.clusterData = QtGui.QLabel('cluster data')
        self.clusterDataEdit = QtGui.QLineEdit()
        self.clusterType = QtGui.QLabel('cluster type')
        self.clusterTypeEdit = QtGui.QComboBox()
        self.clusterTypeEdit.addItem("correlation")
        self.clusterTypeEdit.addItem("braycutis")
        self.clusterTypeEdit.addItem("cosine")
        self.clusterPara = QtGui.QLabel('cluster parameter')
        self.clusterParaEdit = QtGui.QLineEdit()
        self.clusterData = QtGui.QLabel('cluster data')
        self.clusterDataEdit = QtGui.QLineEdit()
        self.clusterBrowse = QtGui.QPushButton("Browse")
        self.clusterButton = QtGui.QPushButton("Clustering")
        self.clusterResult = QtGui.QTextEdit()

        self.mergeTitle = QtGui.QLabel('')
        self.mergeButton = QtGui.QPushButton("Merge Template")
        self.mergeResult = QtGui.QTextEdit()

        self.maskTitle = QtGui.QLabel('')
        self.maskRate = QtGui.QLabel('signal/unused/background')
        self.maskRateEdit = QtGui.QComboBox()
        self.maskRateEdit.addItem("10%/40%/50%")
        self.maskRateEdit.addItem("15%/35%/50%")
        self.maskRateEdit.addItem("20%/30%/50%")
        self.maskRateEdit.addItem("Custom")
        self.maskButton = QtGui.QPushButton("Get mask")
        self.maskResult = QtGui.QTextEdit()
        self.createExitButton = QtGui.QPushButton("Exit")
        
        gridlayout = QtGui.QGridLayout()
        gridlayout.addWidget(self.cropTitle, 0, 0)
        gridlayout.addWidget(self.dataset, 1, 0)
        gridlayout.addWidget(self.datasetEdit, 1, 1)
        gridlayout.addWidget(self.cropBrowse, 1, 2)
        gridlayout.addWidget(self.fileType, 2, 0)
        gridlayout.addWidget(self.fileTypeEdit, 2, 1)
        gridlayout.addWidget(self.output, 3, 0)
        gridlayout.addWidget(self.outputEdit, 3, 1)
        gridlayout.addWidget(self.cropButton, 4, 0)
        gridlayout.addWidget(self.cropResult, 4, 1)

        gridlayout.addWidget(self.clusterTitle, 5, 0)
        gridlayout.addWidget(self.clusterData, 6, 0)
        gridlayout.addWidget(self.clusterDataEdit, 6, 1)
        gridlayout.addWidget(self.clusterBrowse, 6, 2)
        gridlayout.addWidget(self.clusterType, 7, 0)
        gridlayout.addWidget(self.clusterTypeEdit, 7, 1)
        gridlayout.addWidget(self.clusterPara, 8, 0)
        gridlayout.addWidget(self.clusterParaEdit, 8, 1)
        gridlayout.addWidget(self.clusterButton, 9, 0)
        gridlayout.addWidget(self.clusterResult, 9, 1)

        gridlayout.addWidget(self.mergeTitle, 11, 0)
        gridlayout.addWidget(self.mergeButton, 12, 0)
        gridlayout.addWidget(self.mergeResult, 12, 1)
        gridlayout.addWidget(self.maskTitle, 13, 0)
        gridlayout.addWidget(self.maskRate, 14, 0)
        gridlayout.addWidget(self.maskRateEdit, 14, 1)
        gridlayout.addWidget(self.maskButton, 15, 0)
        gridlayout.addWidget(self.maskResult, 15, 1)
        gridlayout.addWidget(self.createExitButton, 16, 1)
        self.setLayout(gridlayout)
        self.connect(self.fileTypeEdit, QtCore.SIGNAL('activated(QString)'), self.onActivated)
        self.connect(self.cropBrowse, QtCore.SIGNAL('clicked()'), self.OnButtonOpen)
        self.connect(self.clusterBrowse, QtCore.SIGNAL('clicked()'), self.OnButtonOpenCluster)
        self.connect(self.cropButton, QtCore.SIGNAL('clicked()'), self.OnButton_crop)
        self.connect(self.clusterButton, QtCore.SIGNAL('clicked()'), self.OnButton_cluster)
        self.connect(self.createExitButton, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))

    def OnCancel(self):
        self.done(0)

    def onActivated(self, text):
        self.fileTypeEdit.setItemText(1, text)
        if text == 'mol2':
            dbpath = self.datasetEdit.text()
            pathList = str(dbpath).split('/')
            databaseName = pathList.pop().split('.')[0]
            self.outputEdit.setText(databaseName)

    def OnButtonOpen(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open')
        if not fileName.isEmpty():
            self.datasetEdit.setText(fileName) 

    def OnButtonOpenCluster(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open')
        if not fileName.isEmpty():
            self.clusterDataEdit.setText(fileName) 

    def process_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--output", help="output path", default="cluster_data.h5", type=str)
        parser.add_argument("-input", help="input path", type=str)
        parser.add_argument("--frame", help="number of frame used", default=50, type=int)
        return parser.parse_args()

    def OnButton_crop(self):
        frame_num = self.fileTypeEdit.text()
        dbpath = self.datasetEdit.text()
        output= self.outputEdit.text()
        args = self.process_args()
        pathList = str(dbpath).split('/')
          
        dialog = MyDialog()       
        pathList.pop()
        args.input = '/'.join(pathList) + '/'
        args.output= str(output)
        args.frame = int(frame_num)
        print(args)
        crop.run(args)
        self.cropResult.setText('result saved at /Users/wyf/Desktop/2d/' + output) 
        dialog.exec_()

    def OnButton_cluster(self):
        frame_num = self.fileTypeEdit.text()
        dbpath = self.datasetEdit.text()
        output = self.outputEdit.text()
        args = self.process_args()
        pathList = str(dbpath).split('/')
          
        dialog = MyDialog()       
        pathList.pop()
        args.input = '/'.join(pathList) + '/'
        args.output = str(output)
        args.frame = int(frame_num)
        print(args)
        peak_cluster.run(args)
        dialog.exec_()


app = QtGui.QApplication(sys.argv) # QApplication eats argv in constructor
win = Window()
win.show()
app.exec_()




