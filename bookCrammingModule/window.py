
from aqt.qt import *
from aqt.utils import showInfo
from aqt import mw
import pickle

class Window(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, None, Qt.Window)
        
        self.form_widget = FormWidget(self, *args) 
        self.setCentralWidget(self.form_widget) 
        
        self.show()
    
    def renderTable(self, wordsToCram):
        self.table = MyTable("mystruct", 100, 10)
        self.table.setMinimumHeight(480)
        self.table.setMinimumWidth(780)
        
        self.table.setmydata(wordsToCram)
        self.table.show()
        
    

class FormWidget(QWidget):
    def __init__(self, parent, *args):        
        super(FormWidget, self).__init__(parent)
        self.logic = args[0]
        self.settings = args[1]
        
        # layout
        self.layout = QGridLayout(self) 
        
        # rank
        self.minRankL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.minRankL.setFont(font)
        self.minRankL.setText("Set rank")
        self.layout.addWidget(self.minRankL,0,0)
        
        self.minRankT = QLineEdit(self)
        self.minRankT.setFixedWidth(100)
        self.layout.addWidget(self.minRankT,0,1)
        
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
        self.outputValL.setText("123")
        self.layout.addWidget(self.outputValL,2,1)
        
        self.minFreqB = QPushButton("Update")
        self.minFreqB.clicked.connect(self.handleButton)
        self.layout.addWidget(self.minFreqB,2,2)
        
        
    
    def handleButton(self):
        self.rankT = int(self.minRankT.text())
        self.freqT = int(self.minFreqT.text())
        self.calculate()
        #winInst.renderTable(wordsToCram)
        
    def calculate(self):
        self.logic.init(self.settings["book_text"])
        self.logic.loadFreq(self.settings["freqCVS"])
        
        runpickle = 0
        if runpickle == 0:
            wordsToCram, stats = self.logic.run(minRank = self.rankT)
            #wordsToCram = self.logic.scanCards(wordsToCram, self.settings["collection"], userKnow=False)
            pik = open('/home/loj/wordsToCram.pkl', 'wb')
            pickle.dump(wordsToCram, pik, pickle.HIGHEST_PROTOCOL)
            pik.close()
        else:
            pik = open('/home/loj/wordsToCram.pkl', 'rb')
            wordsToCram = pickle.load(pik)
        
        
        
        #print g.representWords(wordsToCram)
        
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
                
        self.outputValL.setText("acih:"+str(stats["toLearn"])+" "+str(reportV))
        
        
        
        # 9 2 (4)
        """
        # print sample words which starts from minRank
        for sta in sorted(wordsToCram.items(), key=lambda x:x[1][1][0]["rank"], reverse=False)[:30]:
            print sta
        """
        
        
        
        
class MyTable(QTableWidget):
    def __init__(self, thestruct, *args): 
        QTableWidget.__init__(self, *args)
        #self.data = thestruct
        self.setHorizontalHeaderLabels(['Word Name', 'Deck Name', "Rank", "Interval", "Frequency"])

    def setmydata(self, wordsToCram):
        wordsI = wordsToCram.items()
        for wordi in range(len(wordsI)):
            #word
            newitem = QTableWidgetItem(wordsI[wordi][0])
            self.setItem(wordi, 0, newitem)
            #deck
            if len(wordsI[wordi][1][1][0]["anki"]["ids"]) > 0:
                newitem = QTableWidgetItem("found")
            else:
                newitem = QTableWidgetItem("not found")
            self.setItem(wordi, 1, newitem)
            #rank
            newitem = QTableWidgetItem(str(wordsI[wordi][1][1][0]["rank"]))
            self.setItem(wordi, 2, newitem)
            #interval
            newitem = QTableWidgetItem(str(wordsI[wordi][1][1][0]["anki"]["ivl"]))
            self.setItem(wordi, 3, newitem)
            #frequency
            newitem = QTableWidgetItem(str(wordsI[wordi][1][0]))
            self.setItem(wordi, 4, newitem)
            
            
        


class Browser(QWebView):
    def __init__(self):
        QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)

    def _result_available(self, ok):
        frame = self.page().mainFrame()
        print unicode(frame.toHtml()).encode('utf-8')
