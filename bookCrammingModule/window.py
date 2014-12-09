
from aqt.qt import *
from aqt.utils import showInfo
from aqt import mw
import pickle

class Window(QMainWindow):
    def __init__(self, kwords):
        QMainWindow.__init__(self, None, Qt.Window)
        kwords["winInst"] = self
        self.form_widget = FormWidget(self, kwords) 
        self.setCentralWidget(self.form_widget) 
        
        self.show()
    
    def renderTable(self, wordsToCram, purpose, dArgs):
        
        tc = TableCalculate()
        wordsI, stats = tc.defineData(wordsToCram, purpose, dArgs)
        
        self.table = MyTable("mystruct", stats["wordsNum"], stats["columns"])
        self.table.setMinimumHeight(480)
        self.table.setMinimumWidth(780)
        
        dArgs["wordsI"] = wordsI
        dArgs["stats"] = stats
        
        statLabel = self.table.setmydata(purpose, dArgs)
        self.table.show()
        return statLabel
        
    

class FormWidget(QWidget):
    def __init__(self, parent, kwords):
        super(FormWidget, self).__init__(parent)
        self.logic = kwords["logic"]
        self.settings = kwords["settings"]
        self.winInst = kwords["winInst"]
        
        # layout
        self.layout = QGridLayout(self) 
        
        # rank
        self.minRankL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.minRankL.setFont(font)
        self.minRankL.setText("Set rank")
        self.layout.addWidget(self.minRankL,0,0, 1,2)
        
        self.minRankT = QLineEdit(self)
        self.minRankT.setFixedWidth(100)
        self.layout.addWidget(self.minRankT,0,1, 1,2)
        
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
        self.layout.addWidget(self.outputL,2,0)
        
        self.outputValL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.outputValL.setFont(font)
        self.outputValL.setText("")
        self.layout.addWidget(self.outputValL,2,1, 1,2)
        
        # min rank
        self.minFreqB = QPushButton("Min Rank")
        self.minFreqB.clicked.connect(self.minRankButton)
        self.layout.addWidget(self.minFreqB,3,0)
        
        # words in Anki
        self.inAnkiB = QPushButton("In Anki")
        self.inAnkiB.clicked.connect(self.inAnkiButton)
        self.layout.addWidget(self.inAnkiB,3,1)
        
        # words NOT in Anki
        self.notInAnkiB = QPushButton("Not In Anki")
        self.notInAnkiB.clicked.connect(self.notInAnkiButton)
        self.layout.addWidget(self.notInAnkiB,3, 2)
        
        self.statusL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.statusL.setFont(font)
        self.statusL.setText("")
        self.layout.addWidget(self.statusL,4,0, 1,3)
        
        
        # defaults
        self.minRankT.setText("2500")
        self.minFreqT.setText("2")
    
    def minRankButton(self):
        self.rankT = int(self.minRankT.text())
        self.freqT = int(self.minFreqT.text())
        self.calculate(purpose="minRank")
        
    def inAnkiButton(self):
        self.rankT = int(self.minRankT.text())
        self.freqT = int(self.minFreqT.text())
        self.calculate(purpose="inAnki")
        
    def notInAnkiButton(self):
        self.rankT = int(self.minRankT.text())
        self.freqT = int(self.minFreqT.text())
        self.calculate(purpose="notInAnki")
        
        
    def calculate(self, purpose):
        self.logic.init(self.settings["book_text"])
        self.logic.loadFreq(self.settings["freqCVS"])
        
        runpickle = 0
        if runpickle == 0:
            wordsToCram, stats = self.logic.run(minRank = self.rankT)
            if purpose=="inAnki" or purpose=="notInAnki":
                wordsToCram = self.logic.scanCards(wordsToCram, self.settings["collection"], userKnow=False)
            pik = open('/home/loj/wordsToCram.pkl', 'wb')
            pickle.dump(wordsToCram, pik, pickle.HIGHEST_PROTOCOL)
            pik.close()
        else:
            pik = open('/home/loj/wordsToCram.pkl', 'rb')
            wordsToCram = pickle.load(pik)
        
        
        
        #print self.logic.representWords(wordsToCram, purpose="minRank")
        
        report = [1, 2, 5, 10]
        reportV = []
        ri=0
        print stats["freq_numToLearn"]
        for t in range(len(stats["freq_numToLearn"])-2, -1, -1):
            if report[ri] <= stats["freq_numToLearn"][t+1][0] and report[ri] < stats["freq_numToLearn"][t][0]:
                reportV.append(stats["freq_numToLearn"][t+1])
                ri+=1
                if len(report) == ri:
                    break
            else:
                continue
                
        self.outputValL.setText(str(reportV))
        
        if purpose=="minRank":
            dArgs = {"minFreq":self.freqT}
        elif purpose=="inAnki":
            dArgs = {"minFreq":self.freqT}
        elif purpose=="notInAnki":
            dArgs = {"minFreq":self.freqT}
        else:
            dArgs = {}
        
        statLabel = self.winInst.renderTable(wordsToCram, purpose, dArgs)
        self.statusL.setText("Words shown:%i" % statLabel["wordsNum"])
        # 9 2 (4)
        """
        TODO what to do with "working" "worked"
        (part of speach) and if it's verb then stem it; if it's adj then add it in anki as adj
        """
        
        
        
class TableCalculate():
    def defineData(self, wordsToCram, purpose, dArgs):
        stats = {}
        if purpose == "minRank":
            words =  sorted([x for x in wordsToCram.items() if x[1][0] >= dArgs["minFreq"]], key=lambda x:x[1][1][0]["rank"], reverse=False)
            labels = ['Word Name', "Rank", "Frequency"]
            
        elif purpose == "notInAnki":
            words =  sorted([x for x in wordsToCram.items() if len(x[1][1][0]["anki"]["ids"]) == 0 and x[1][0] >= dArgs["minFreq"]]
                                                            , key=lambda x:x[1][1][0]["rank"], reverse=False)
            labels = ['Word Name', "Rank", "Frequency"]
        elif purpose == "inAnki":
            words =  sorted([x for x in wordsToCram.items() if len(x[1][1][0]["anki"]["ids"]) >= 1 and x[1][0] >= dArgs["minFreq"]]
                                                            , key=lambda x:x[1][1][0]["rank"], reverse=False)
            labels = ['Word Name', "Rank", "Interval", "Frequency"]
        
        stats["wordsNum"] = len(words)
        stats["columns"] = len(labels)
        stats["labels"] = labels
        
        
        return words, stats
    
class MyTable(QTableWidget):
    def __init__(self, thestruct, *args): 
        QTableWidget.__init__(self, *args)
        

    def setmydata(self, purpose, dArgs):
        self.setHorizontalHeaderLabels(dArgs["stats"]["labels"])
        
        wordsI = dArgs["wordsI"]
        for wordi in range(len(wordsI)):
            columNum=0
            if purpose == "minRank":
                self.setWordName(wordsI, wordi, columNum); columNum += 1
                self.setRank(wordsI, wordi, columNum); columNum += 1
                self.setFreq(wordsI, wordi, columNum); columNum += 1
                
            elif purpose == "inAnki":
                self.setWordName(wordsI, wordi, columNum); columNum += 1
                self.setRank(wordsI, wordi, columNum); columNum += 1
                self.setIvl(wordsI, wordi, columNum); columNum += 1
                self.setFreq(wordsI, wordi, columNum); columNum += 1
                
            elif purpose == "notInAnki":
                self.setWordName(wordsI, wordi, columNum); columNum += 1
                self.setRank(wordsI, wordi, columNum); columNum += 1
                self.setFreq(wordsI, wordi, columNum); columNum += 1
                
                
        return dArgs["stats"]
            
            
            
        
    def setAnkiHits(self, wordsI, wordi, columNum):
        newitem = QTableWidgetItem(str(len(wordsI[wordi][1][1][0]["anki"]["ids"])))
        self.setItem(wordi, columNum, newitem)
    
    def setWordName(self, wordsI, wordi, columNum):
        newitem = QTableWidgetItem(wordsI[wordi][0])
        self.setItem(wordi, columNum, newitem)
    
    def setRank(self, wordsI, wordi, columNum):
        newitem = QTableWidgetItem(str(wordsI[wordi][1][1][0]["rank"]))
        self.setItem(wordi, columNum, newitem)
    
    def setFreq(self, wordsI, wordi, columNum):
        newitem = QTableWidgetItem(str(wordsI[wordi][1][0]))
        self.setItem(wordi, columNum, newitem)
    
    def setIvl(self, wordsI, wordi, columNum):
        newitem = QTableWidgetItem(str(wordsI[wordi][1][1][0]["anki"]["ivl"]))
        self.setItem(wordi, columNum, newitem)

