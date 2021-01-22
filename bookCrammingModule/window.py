# import all of the Qt GUI library
from aqt.qt import *
# import the "show info" tool from utils.py
from aqt.utils import showInfo
from aqt import mw
import anki
import pickle, codecs

class Window(QMainWindow):
    def __init__(self, kwords):
        QMainWindow.__init__(self, None, Qt.Window)
        kwords["winInst"] = self
        self.myWin = kwords["my_window"]
        self.form_widget = FormWidget(self, kwords) 
        self.setCentralWidget(self.form_widget) 
        self.show()

    def renderTable(self, purpose, wordsI, labels):
        statLabel = {"wordsNum": len(wordsI), "columns": len(labels), "labels": labels}

        self.table = MyTable("mystruct", statLabel["wordsNum"], statLabel["columns"])
        self.table.setMinimumHeight(480)
        self.table.setMinimumWidth(780)
        self.table.setmydata(purpose, wordsI, statLabel)
        self.table.show()
        return wordsI, statLabel

    def canClose(self):
        return True
    def close(self):
        return True
    def closeWithCallback(self, callback):
        self.myWin[1] = None
        callback()

class FormWidget(QWidget):
    def __init__(self, parent, kwords):
        super(FormWidget, self).__init__(parent)
        self.textLogic = kwords["textLogic"]
        self.ankiLogic = kwords["ankiLogic"]
        self.settings = kwords["settings"]
        self.winInst = kwords["winInst"]
        
        # layout
        self.layout = QGridLayout(self) 
        
        # rank
        self.checkWordsL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.checkWordsL.setFont(font)
        self.checkWordsL.setText("Set rank")
        self.layout.addWidget(self.checkWordsL,0,0, 1,2)
        
        self.checkWordsT = QLineEdit(self)
        self.checkWordsT.setFixedWidth(100)
        self.layout.addWidget(self.checkWordsT,0,1, 1,2)
        
        # frequency
        self.minFreqL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.minFreqL.setFont(font)
        self.minFreqL.setText("Set freq")
        self.layout.addWidget(self.minFreqL,1,0)
        
        self.minFreqT = QLineEdit(self)
        self.minFreqT.setFixedWidth(100)
        self.layout.addWidget(self.minFreqT,1,1)

        # output
        self.outputL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.outputL.setFont(font)
        self.outputL.setText("To learn(freq:num):")
        self.layout.addWidget(self.outputL,3,0)

        self.outputValL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.outputValL.setFont(font)
        self.outputValL.setText("")
        self.layout.addWidget(self.outputValL,3,1, 1,2)

        # output1
        self.outputL1 = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.outputL1.setFont(font)
        self.outputL1.setText("To learn(rank:num):")
        self.layout.addWidget(self.outputL1, 4, 0)
        
        self.outputValL1 = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.outputValL1.setFont(font)
        self.outputValL1.setText("")
        self.layout.addWidget(self.outputValL1,4,1, 1,2)

        # check words
        self.minFreqB = QPushButton("Check Words")
        self.minFreqB.clicked.connect(self.checkWordsButton)
        self.layout.addWidget(self.minFreqB,5,0)

        # not in freq list
        self.notInFreqB = QPushButton("Not in Freq")
        self.notInFreqB.clicked.connect(self.notInFreqButton)
        self.layout.addWidget(self.notInFreqB,5, 1)

        ###
        self.statusL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.statusL.setFont(font)
        self.statusL.setText("Words shown:")
        self.layout.addWidget(self.statusL,6,0)
        
        # set definitions (new cards with links to online dictionaries)
        self.setDefinitionsB = QPushButton("Set Definitions")
        self.setDefinitionsB.clicked.connect(self.setDefinitionsButton)
        self.layout.addWidget(self.setDefinitionsB,7, 0)

        # another status bar
        self.status1L = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.status1L.setFont(font)
        self.status1L.setText("Status: OK")
        self.layout.addWidget(self.status1L,8,0, 1, 3)
        
        # defaults
        self.checkWordsT.setText("2500")
        self.minFreqT.setText("2")

    def parseTextFields(self):
        self.rankTV = int(self.checkWordsT.text())
        self.minFreq = int(self.minFreqT.text())
    
    def checkWordsButton(self):
        self.parseTextFields()
        self.calculate(purpose="checkWords")
        
    def notInFreqButton(self):
        self.parseTextFields()
        self.calculate(purpose="notInFreq")
        
    def inAnkiButton(self):
        self.parseTextFields()
        self.calculate(purpose="inAnki")

    def setDefinitionsButton(self):
        # read data from window (for checked items)
        listOfWords = []
        if not hasattr(self.winInst, "table"):
            self.status1L.setText("Status: please run a task and tick some cards.")
            return
        for row in range(self.winInst.table.rowCount()):
            wordText = self.winInst.table.item(row, 0).text()
            if self.winInst.table.item(row, 0).checkState() == 2:  # 2 checked, 0 unchecked
                listOfWords.append(wordText)

        statistics = self.ankiLogic.setDefinitions(listOfWords)

        self.status1L.setText("Status: updated %i, added %i, refreshed %i" % (
            statistics["updated"], statistics["added"], statistics["refreshed"]))

    def notInAnkiButton(self):
        self.parseTextFields()
        self.calculate(purpose="notInAnki")

    def calculate(self, purpose):
        wordsToCram, notInFreq, stats = self.textLogic.run(minRank=self.rankTV)
        self.outputValL.setText(str(self.textLogic.prepareToLearn(stats)))
        self.outputValL1.setText(str(self.textLogic.prepareToLearn1(wordsToCram, self.minFreq)))

        if purpose == "checkWords":
            labels = ['Word Name', "Rank", "Frequency"]
            wordsI = sorted([x for x in list(wordsToCram.items()) if x[1][0] >= self.minFreq],
                            key=lambda x: x[1][1][0]["rank"], reverse=False)
            wordList, statLabel = self.winInst.renderTable(purpose, wordsI, labels)
        elif purpose == "notInFreq":
            #  if wordsToCram.has_key(x[0]) and len(wordsToCram[x[0]][1][0]["anki"]["ids"]) == 0
            labels = ['Word Name', "Frequency"]
            wordsI = sorted([x for x in list(notInFreq.items())],
                            key=lambda x: x[1], reverse=True)
            wordList, statLabel = self.winInst.renderTable(purpose, wordsI, labels)

        self.statusL.setText("Words shown:%i" % statLabel["wordsNum"])

class MyTable(QTableWidget):
    def __init__(self, thestruct, *args):
        QTableWidget.__init__(self, *args)

    def setmydata(self, purpose, wordsI, stats):
        self.setHorizontalHeaderLabels(stats["labels"])

        for wordi in range(len(wordsI)):
            columNum=0
            if purpose == "checkWords":
                self.setWordName(wordsI, wordi, columNum); columNum += 1
                self.setRank(wordsI, wordi, columNum); columNum += 1
                self.setFreq(wordsI, wordi, columNum); columNum += 1
            elif purpose == "notInFreq":
                self.setWordName(wordsI, wordi, columNum, purpose="notInFreq"); columNum += 1
                self.setFreq(wordsI, wordi, columNum, purpose="notInFreq"); columNum += 1

    def setWordName(self, wordsI, wordi, columNum, purpose=None):
        display_string = wordsI[wordi][0]
        newitem = QTableWidgetItem(display_string)
        newitem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        if purpose=="notInFreq":
            newitem.setCheckState(Qt.Unchecked)
        else:
            newitem.setCheckState(Qt.Checked)
        self.setItem(wordi, columNum, newitem)

    def setRank(self, wordsI, wordi, columNum):
        newitem = QTableWidgetItem(str(wordsI[wordi][1][1][0]["rank"]))
        self.setItem(wordi, columNum, newitem)

    def setFreq(self, wordsI, wordi, columNum, purpose=None):
        if purpose=="notInFreq":
            display_string = str(wordsI[wordi][1])
        else:
            display_string = str(wordsI[wordi][1][0])
        self.setItem(wordi, columNum, QTableWidgetItem(display_string))

    def setIvl(self, wordsI, wordi, columNum):
        ivl = str(wordsI[wordi][1][1][0]["anki"]["ivl"])
        self.setItem(wordi, columNum, QTableWidgetItem(ivl))

