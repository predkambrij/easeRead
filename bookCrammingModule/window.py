
from aqt.qt import *
from aqt.utils import showInfo
from aqt import mw

class Window(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, None, Qt.Window)
        #showInfo("Test content")
        """
        layout = QGridLayout() 
        self.led = QLineEdit("Sample")
        
        self.table = QTableWidget()
        self.table.setRowCount(5)
        self.table.setColumnCount(5)
        layout.addWidget(self.led, 0, 0)
        layout.addWidget(self.table, 1, 0)
        self.table.setItem(1, 0, QTableWidgetItem(self.led.text()))
        """
        """
        layout = QGridLayout() 
        self.led = QLineEdit("Sample")
        
        layout.addWidget(self.led, 0, 0)
        layout.addWidget(self.table, 1, 0)
        self.table.setItem(1, 0, QTableWidgetItem(self.led.text()))
        self.setLayout(layout)
        """
        
        #self.splitter = QtGui.QSplitter(self.splitter_2)
        #self.widget = QtGui.QWidget(self.splitter)
        self.centralwidget = QWidget()
        self.tableView = QTableView(self)
        #self.centralwidget.exec_()
        
        self.button = QPushButton('Test', self)
        self.button.clicked.connect(self.handleButton)
        
        """
        self.table = QTableWidget()
        self.table.setRowCount(5)
        self.table.setColumnCount(5)
        """
        
        
        #layout = QGridLayout() 
        layout = QVBoxLayout(self)
        
        """
        self.tableView = QTableView(self)
        self.tableView.setMinimumSize(QSize(0, 150))
        self.tableView.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableView.setFrameShape(QFrame.NoFrame)
        self.tableView.setFrameShadow(QFrame.Plain)
        self.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setTabKeyNavigation(False)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setCascadingSectionResizes(False)
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.horizontalHeader().setMinimumSectionSize(20)
        self.tableView.horizontalHeader().setSortIndicatorShown(True)
        """
        self.label_nombre = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_nombre.setFont(font)
        self.label_nombre.setObjectName("label_nombre")
        self.label_nombre.setText("hola")
        
        #layout.addWidget(self.table)
        #layout.addWidget(self.tableView)
        layout.addWidget(self.button)
        layout.addWidget(self.label_nombre)
        self.show()
    
    def renderTable(self, wordsToCram):
        self.table = MyTable("mystruct", 100, 10)
        self.table.setMinimumHeight(480)
        self.table.setMinimumWidth(780)
        
        self.table.setmydata(wordsToCram)
        self.table.show()
        
    def handleButton(self):
        print ('Hello World')


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
