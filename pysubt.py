
import sys
import re
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QTextEdit, QLineEdit, QLabel, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon


class subtitle_entry():
    def __init__(self):
        print("init")
        self.starttime = "000"
        self.stoptime = "0000"
        self.subtext = ""
        self.index = 0
        
    def getPrintString():
        retVal = ""
        retVal = retVal + self.index + "," + self.starttime + "," + self.stoptime + "," + self.subtext
        return retVal
        
    
class SubtitleMaker(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.entries = []
        self.fnam = ""
        
        self.initUI()
              
    def initUI(self): 
    
        self.lb_idx = QLabel('Index:',self)
        self.lb_idx.move(15,270)
        
        lbl1 = QLabel('Start:', self)
        lbl1.move(15, 25)
        
        lbl2 = QLabel('Stop:', self)
        lbl2.move(240, 25)
        
        lbl3 = QLabel('Text:', self)
        lbl3.move(15, 80)
        
        self.startEdit = QLineEdit(self)
        self.startEdit.move(15,50)
        self.startEdit.resize(170,20)
        
        self.stopEdit = QLineEdit(self)
        self.stopEdit.move(240,50)
        self.stopEdit.resize(170,20)
        
        self.te = QTextEdit(self)
        self.te.move(15,105)
        self.te.resize(400,170)
        
        self.nextButton = QPushButton("Next",self)
        self.nextButton.move(20,300)
        self.nextButton.resize(80,20)
        self.nextButton.clicked.connect(self.nextEntry)
        
        self.clearButton = QPushButton("Clear",self) 
        self.clearButton.move(120,300)
        self.clearButton.resize(80,20)
        self.clearButton.clicked.connect(self.clearTextfields)
        
        self.quitButton = QPushButton("Quit",self)    
        self.quitButton.move(220,300)
        self.quitButton.resize(80,20)
        self.quitButton.clicked.connect(qApp.quit)
    
        # create new Action
        newAct = QAction(QIcon('new.png'),'&New',self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip('New Subtitlefile')
        newAct.triggered.connect(self.newFile)
        
        # create open Action
        openAct = QAction(QIcon('new.png'),'&Open',self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open Subtitlefile')
        openAct.triggered.connect(self.openFile)
        
        #create generate action
        genAct = QAction(QIcon('new.png'),'&Generate srt',self)
        genAct.setShortcut('Ctrl+G')
        genAct.setStatusTip('generate srt file')
        genAct.triggered.connect(self.generatesrt)
        
        # create exit Action
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAct)
        fileMenu.addAction(openAct)
        fileMenu.addAction(genAct)
        fileMenu.addAction(exitAct)	
        
        self.statusBar().showMessage('Ready')
        
        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Simple Subtitles - v0.01')    
        self.show()
    
    def nextEntry(self):
        print("next")
        starttime = self.startEdit.text()
        stoptime = self.stopEdit.text()
        subtext = self.te.toPlainText()
        if not self.isSubtitleTime(starttime):
            return
        if not self.isSubtitleTime(stoptime):
            return
            
        if len(subt_text) <= 0 :
            return
             
    def newFile(self):
        print('new file')
        self.fnam = self.__saveFileDialog()
        f = open(self.fnam,"w")
        f.close()
        
    def openFile(self):
        print('open file')
        fnam = self.__openFileNameDialog()
        if self.readinsrtfile(fnam):
            self.fnam = fnam
          
    def generatesrt(self):
        print("generate")
    
    def readinsrtfile(self,filename):
        num_pattern = re.compile("^\d+$")
        one_time_pattern = re.compile("\d\d\:\d\d\:\d\d,\d\d\d")
        times_pattern = re.compile("^\d\d:\d\d:\d\d,\d\d\d\s\-\->\s+\d\d:\d\d:\d\d,\d\d\d$")
        text_pattern = re.compile("^[\w\s]+")
        empty_line_pattern = re.compile("^$")
        mystate = 'index'
        index = ""
        starttime =""
        stoptime = ""
        subtext = ""
        
        with open(filename,"r") as lines:
            for line in lines:
                if mystate == 'index':
                    tmatch = num_pattern.search(line)
                    if tmatch:
                        index = line.rstrip("\n")
                        mystate = 'times'
                elif mystate == 'times':
                    tmatch = one_time_pattern.findall(line)
                    if tmatch:
                        starttime = tmatch[0]
                        stoptime = tmatch[1]
                        
                        mystate = 'text'
                elif mystate == 'text':
                    tmatch = text_pattern.search(line)
                    tmatch2 = empty_line_pattern.search(line)
                    if tmatch:
                        subtext = subtext + line
                    if tmatch2:
                        se = subtitle_entry()
                        se.index = index
                        se.starttime = starttime
                        se.stoptime = stoptime
                        se.subtext = subtext
                        self.entries.append(se)
                        
                        mystate = 'index'
     
        print("subts read",len(self.entries))
        return True
        
    def __checkEntrySanity(self):
        retVal = False
        if len(self.entries) <= 0:
            return False
        last_index = -1
        last_starttime = ""
        last_stoptime = ""
        
        for en in self.entries:
            idx = en.index
            startT = en.starttime
            stopT = en.stoptime
            
        return retVal
    
    def __getTimeFromSubTime(self,subtime):
        zeug = re.split("[:,]+",subtime)
        stund = zeug[0]
        minut = zeug[1]
        sekund = zeug[2]
        millisekund = zeug[3]
        
              
    def isSubtitleTime(self,input):
        retVal = False
        
        tmatch = re.search(input,"\d\d:\d\d:\d\d,\d\d\d")
        if tmatch:
            retVal = True
        
        return retVal
        
    def clearTextfields(self):
        self.startEdit.clear()
        self.stopEdit.clear()
        self.te.clear()
        
    def __openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","", options=options)
        if fileName:
            #print(fileName)
            return fileName
        
        return ""
        
    def __saveFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","srt Files (*.srt);;All Files (*)", options=options)
        if fileName:
            print(fileName)
            return fileName
        
        return ""
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = SubtitleMaker()
    sys.exit(app.exec_())
    
    
