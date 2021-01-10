
from aqt.qt import *
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
        
        # min anki interval
        self.minIvlL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.minIvlL.setFont(font)
        self.minIvlL.setText("Min anki ivl")
        self.layout.addWidget(self.minIvlL,2,0)
        
        self.minIvlT = QLineEdit(self)
        self.minIvlT.setFixedWidth(100)
        self.layout.addWidget(self.minIvlT,2,1)
        
        
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
        
        # min rank
        self.minFreqB = QPushButton("Min Rank")
        self.minFreqB.clicked.connect(self.minRankButton)
        self.layout.addWidget(self.minFreqB,4,0)
        
        # words in Anki
        self.inAnkiB = QPushButton("In Anki")
        self.inAnkiB.clicked.connect(self.inAnkiButton)
        self.layout.addWidget(self.inAnkiB,4,1)
        
        # words NOT in Anki
        self.notInAnkiB = QPushButton("Not In Anki")
        self.notInAnkiB.clicked.connect(self.notInAnkiButton)
        self.layout.addWidget(self.notInAnkiB,4, 2)
        
        
        # tag words in Anki
        self.notInAnkiB = QPushButton("Tag with #%s"%self.settings["hashTag"])
        self.notInAnkiB.clicked.connect(self.tagButton)
        self.layout.addWidget(self.notInAnkiB,5, 1)
        
        # untag all
        self.notInAnkiB = QPushButton("Untag all")
        self.notInAnkiB.clicked.connect(self.unTagButton)
        self.layout.addWidget(self.notInAnkiB,5, 2)
        
        self.statusL = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.statusL.setFont(font)
        self.statusL.setText("Words shown:")
        self.layout.addWidget(self.statusL,5,0)
        
        # set definitions (new cards with links to online dictionaries)
        self.setDefinitionsB = QPushButton("Set Definitions")
        self.setDefinitionsB.clicked.connect(self.setDefinitionsButton)
        self.layout.addWidget(self.setDefinitionsB,6, 0)
        
        # not in freq list
        self.notInFreqB = QPushButton("Not in Anki nor Freq list")
        self.notInFreqB.clicked.connect(self.notInFreqButton)
        self.layout.addWidget(self.notInFreqB,6, 1)
        
        # blacklist
        self.blacklistB = QPushButton("Blacklist selected")
        self.blacklistB.clicked.connect(self.blacklistButton)
        self.layout.addWidget(self.blacklistB,6, 2)
        
        # another status bar
        self.status1L = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.status1L.setFont(font)
        self.status1L.setText("Status: OK")
        self.layout.addWidget(self.status1L,7,0, 1, 3)
        
        
        # defaults
        self.minRankT.setText("2500")
        self.minFreqT.setText("2")
        self.minIvlT.setText("2")
    
    def parseTextFields(self):
        self.rankTV = int(self.minRankT.text())
        self.freqTV = int(self.minFreqT.text())
        self.minIvlTV = int(self.minIvlT.text())
    
    def minRankButton(self):
        self.parseTextFields()
        self.calculate(purpose="minRank")
        
    def notInFreqButton(self):
        self.parseTextFields()
        self.calculate(purpose="notInFreq")
        
    def inAnkiButton(self):
        self.parseTextFields()
        self.calculate(purpose="inAnki")
        
    def getDeckNotes(self):
        ft = anki.find.Finder(self.settings["collection"])
        notesIDs = ft.findNotes('deck:"%s"'%self.settings["dictDeckName"])
        notes = []
        for noteId in notesIDs:
            notes.append(mw.col.getNote(noteId))
        return notes
    
    def templateBack(self, word):
        back = (("<a href='http://www.oxforddictionaries.com/definition/english/%s'>Oxford</a>" % word.replace(" ", "-"))+
                ("&nbsp;&nbsp;<a href='http://dictionary.cambridge.org/dictionary/british/%s'>Cambridge</a>" % word.replace(" ", "-"))+
                ("&nbsp;&nbsp;<a href='https://www.google.com/search?tbm=isch&q=%s'>Images</a>" % word)+
                ("")
                )
        return back
    def addOrUpdateWord(self, deckId, notes, word=None, updateAll=False):
        statistics = {"updated":0, "added":0, "refreshed":0}
        for note in notes:
            if updateAll == True:
                note["Back"] = self.templateBack(note["Front"])
                statistics["refreshed"] += 1
                note.flush()
            else:
                if note["Front"] == word:
                    note["Back"] = self.templateBack(note["Front"])
                    note.flush()
                    statistics["updated"] += 1
                    return statistics
        
        if updateAll == True:
            return statistics
        # it's not in collection yet, let's add it then
        note = mw.col.newNote()
        note["Front"] = word
        note["Back"] = self.templateBack(note["Front"])
        note.model()['did'] = deckId
        cards = mw.col.addNote(note)
        statistics["added"] += 1
        
        return statistics
    
    def readNotInFreq(self):
        """
        cbDefNum - num of definitions from cambridge dictionary (-1 means not requested yet)
        checked - if user checked item in table (if the user wants to add it in anki or not)
        """
        notInFreq = {}
        for line in codecs.open(self.settings["notInFreqDb"], "rb", encoding="utf-8"):
                word,checked,cbDefNum = line.split("\t")
                notInFreq[word] = {"checked":int(checked), "cbDefNum":int(cbDefNum)}
        return notInFreq
    
    def writeNotInFreq(self, notInFreq):
        """
        cbDefNum - num of definitions from cambridge dictionary (-1 means not requested yet)
        checked - if user checked item in table (if the user wants to add it in anki or not)
        """
        strBuild = ""
        for word, props in [(x[0], x[1]) for x in list(notInFreq.items())]:
            strBuild += "%s\t%s\t%s\n" % (word, str(props["checked"]), str(props["cbDefNum"]))
        codecs.open(self.settings["notInFreqDb"], "wb", encoding="utf-8").write(strBuild)
        return
    
    def setDefinitionsButton(self):
        # read data from window (for checked items)
        listOfWords = []
        if not hasattr(self.winInst, "table"):
            self.status1L.setText("Status: please run \"Not In Anki\" or \"Not in Anki nor Freq list\" first")
            return
        
        if self.winInst.table.lastPurpose == "notInFreq":
            notInFreqDb = self.winInst.table.notInFreqDb
            for row in range(self.winInst.table.rowCount()):
                wordText = self.winInst.table.item(row,0).text()
                if self.winInst.table.item(row,0).checkState() == 2: # checked
                    listOfWords.append(wordText)
                    if wordText in notInFreqDb:
                        notInFreqDb[wordText]["checked"] = 2
                    else:
                        notInFreqDb[wordText] = {"checked":2, "cbDefNum":-1}
                    
                elif self.winInst.table.item(row,0).checkState() == 0: # unchecked
                    if wordText in notInFreqDb:
                        notInFreqDb[wordText]["checked"] = 0
                    else:
                        notInFreqDb[wordText] = {"checked":0, "cbDefNum":-1}
            
            # write state of the table in file
            self.writeNotInFreq(notInFreqDb)
        elif self.winInst.table.lastPurpose != "notInAnki":
            self.status1L.setText("Status: please run \"Not In Anki\" or \"Not in Anki nor Freq list\" first, other results detected")
            return
        elif self.winInst.table.lastPurpose == "notInAnki":
            for row in range(self.winInst.table.rowCount()):
                if self.winInst.table.item(row,0).checkState() == 2:
                    listOfWords.append(self.winInst.table.item(row,0).text())
        else:
            # something is fundamentally wrong
            return
        
        
        deckId = mw.col.decks.id("%s" % self.settings["dictDeckName"])
        #deck = mw.col.decks.get(deckId)
        notes = self.getDeckNotes()
        statistics = {"updated":0, "added":0, "refreshed":0}
        for word in listOfWords:
            res = self.addOrUpdateWord(deckId, notes, word)
            statistics["updated"] += res["updated"]
            statistics["added"] += res["added"]
            
            
        res = self.addOrUpdateWord(deckId, notes, updateAll=True)
        statistics["refreshed"] += res["refreshed"]
        self.status1L.setText("Status: updated %i, added %i, refreshed %i" % (
            statistics["updated"], statistics["added"], statistics["refreshed"]))
        
    def notInAnkiButton(self):
        self.parseTextFields()
        self.calculate(purpose="notInAnki")
    
    def tagButton(self):
        # untag that we ensure that there're no duplicate tags
        self.unTagButton()
        
        self.parseTextFields()
        self.calculate(purpose="tagList")
        
    def unTagButton(self):
        self.parseTextFields()
        #self.calculate(purpose="unTag")
        
        ft = anki.find.Finder(self.settings["collection"])
        cardIds = ft.findCards("tag:%s"%self.settings["hashTag"])
        ankiNoteIds = set([])
        for cardId in cardIds:
            card = mw.col.getCard(cardId)
            ankiNoteIds.add(card.nid)
        self.settings["collection"].tags.bulkRem(list(ankiNoteIds), self.settings["hashTag"])
        
        
    def tagWords(self, wordList):
        ankiNoteIds = set([])
        for word in wordList:
            ankiNoteIds |= set(word[1][1][0]["anki"]["nids"])
        print(ankiNoteIds)
        self.settings["collection"].tags.bulkAdd(list(ankiNoteIds), self.settings["hashTag"])
        return
    
    def readBlacklistMapping(self):
        """
        set key of dict and possibility for new data
        """
        mapping = {}
        
        for line in codecs.open(self.settings["blacklisted_man_text"], "rb", encoding="utf-8"):
                word = line.split("|", 1)
                if len(word) == 2:
                    if len(word[0]) > 1:
                        mapping[word[0].strip()] = [ x.strip() for x in word[1].split(",")]
        return mapping
    
    def calculate(self, purpose):
        self.logic.init(self.settings["book_text"])
        self.logic.loadFreq1(self.settings["freqCVS"])
        
        runpickle = 0
        if runpickle == 0:
            wordsToCram, stats, notInFreq = self.logic.run(minRank = self.rankTV, blMap=self.readBlacklistMapping())
            if purpose=="inAnki" or purpose=="tagList":
                wordsToCram = self.logic.scanCards(wordsToCram, self.settings["collection"], ankiIvl=self.minIvlTV)
            elif purpose=="notInAnki" or purpose=="setDefinitions" or purpose=="notInFreq":
                wordsToCram = self.logic.scanCards(wordsToCram, self.settings["collection"], ankiIvl=None)
            pik = open('/home/user/wordsToCram.pkl', 'wb')
            pickle.dump(wordsToCram, pik, pickle.HIGHEST_PROTOCOL)
            pik.close()
        else:
            pik = open('/home/user/wordsToCram.pkl', 'rb')
            wordsToCram = pickle.load(pik)
        
        # remove blacklisted from displaying
        blacklisted = self.readBlacklist()
        for word, props in list(blacklisted.items()):
            if word in wordsToCram:
                del wordsToCram[word]
        
        #print self.logic.representWords(wordsToCram, purpose="minRank")
        
        report = [1, 2, 5, 10]
        reportV = []
        ri=0
        #print stats["freq_numToLearn"]
        for t in range(len(stats["freq_numToLearn"])-2, -1, -1):
            if report[ri] <= stats["freq_numToLearn"][t+1][0] and report[ri] < stats["freq_numToLearn"][t][0]:
                reportV.append(stats["freq_numToLearn"][t+1])
                ri+=1
                if len(report) == ri:
                    break
            else:
                continue
                
        self.outputValL.setText(str(reportV))
        
        if purpose=="notInFreq":
            for word, props in list(blacklisted.items()):
                if word in notInFreq:
                    del notInFreq[word]
            
            dArgs = {"minFreq":self.freqTV,
                     "notInFreq":notInFreq,
                     "wtc":wordsToCram,
                     "notInFreqDb":self.readNotInFreq()}
        else:
            dArgs = {"minFreq":self.freqTV}
        
        
        wordList, statLabel = self.winInst.renderTable(wordsToCram, purpose, dArgs)
        self.statusL.setText("Words shown:%i" % statLabel["wordsNum"])
        
        if purpose == "tagList":
            self.tagWords(wordList)
        
            
        # 9 2 (4)
        """
        TODO what to do with "working" "worked"
        (part of speach) and if it's verb then stem it; if it's adj then add it in anki as adj
        """
    def readBlacklist(self):
        """
        set key of dict and possibility for new data
        """
        blacklist = {}
        for line in codecs.open(self.settings["blacklisted_text"], "rb", encoding="utf-8"):
                word = line.split("\t", 1)
                blacklist[word[0].strip()] = {}
        for line in codecs.open(self.settings["blacklisted_man_text"], "rb", encoding="utf-8"):
                word = line.split("|", 1)
                if len(word[0]) > 1:
                    blacklist[word[0].strip()] = {}
        return blacklist
    
    def writeBlacklist(self, blacklist):
        """
        """
        strBuild = ""
        for word, props in sorted([(x[0], x[1]) for x in list(blacklist.items())], key=lambda x:x[0]):
            strBuild += "%s\t%s\n" % (word, "1")
        codecs.open(self.settings["blacklisted_text"], "wb", encoding="utf-8").write(strBuild)
        return
    
    def blacklistButton(self):
        # read data from window (for checked items)
        listOfWords = []
        if not hasattr(self.winInst, "table"):
            self.status1L.setText("Status: please run \"Not In Anki\" or \"Not in Anki nor Freq list\" first")
            return
        
        if self.winInst.table.lastPurpose == "notInFreq" or self.winInst.table.lastPurpose == "notInAnki":
            for row in range(self.winInst.table.rowCount()):
                if self.winInst.table.item(row,0).checkState() == 2:
                    listOfWords.append(self.winInst.table.item(row,0).text())
        else:
            self.status1L.setText("Status: please run \"Not In Anki\" or \"Not in Anki nor Freq list\" first")
            return
        
        blacklist = self.readBlacklist()
        
        for word in listOfWords:
            blacklist[word] = {}
        self.writeBlacklist(blacklist)
        self.status1L.setText("Status: successfully blacklisted, remove from ...."+
                              self.settings["blacklisted_text"][self.settings["blacklisted_text"].rfind("/"):]
                              +" if you did the mistake")
        
        
class TableCalculate():
    def defineData(self, wordsToCram, purpose, dArgs):
        stats = {}
        if purpose == "minRank":
            words =  sorted([x for x in list(wordsToCram.items()) if x[1][0] >= dArgs["minFreq"]], key=lambda x:x[1][1][0]["rank"], reverse=False)
            labels = ['Word Name', "Rank", "Frequency"]
            
        elif purpose == "notInAnki":
            words =  sorted([x for x in list(wordsToCram.items()) if len(x[1][1][0]["anki"]["ids"]) == 0 and x[1][0] >= dArgs["minFreq"]]
                                                            , key=lambda x:x[1][1][0]["rank"], reverse=False)
            labels = ['Word Name', "Rank", "Frequency"]
        elif purpose == "inAnki" or purpose == "tagList":
            words =  sorted([x for x in list(wordsToCram.items()) if len(x[1][1][0]["anki"]["ids"]) >= 1 and x[1][0] >= dArgs["minFreq"]]
                                                            , key=lambda x:x[1][1][0]["rank"], reverse=False)
            labels = ['Word Name', "Rank", "Interval", "Frequency"]
        elif purpose == "notInFreq":
            #  if dArgs["wtc"].has_key(x[0]) and len(dArgs["wtc"][x[0]][1][0]["anki"]["ids"]) == 0
            words = sorted([x for x in list(dArgs["notInFreq"].items())], key=lambda x:x[1], reverse=True)
            labels = ['Word Name', "Frequency"]
            
        stats["wordsNum"] = len(words)
        stats["columns"] = len(labels)
        stats["labels"] = labels
        
        return words, stats
    
class MyTable(QTableWidget):
    def __init__(self, thestruct, *args): 
        QTableWidget.__init__(self, *args)
        

    def setmydata(self, purpose, dArgs):
        self.lastPurpose = purpose
        self.setHorizontalHeaderLabels(dArgs["stats"]["labels"])
        
        if purpose == "notInFreq":
            self.notInFreqDb = dArgs["notInFreqDb"]
        
        wordsI = dArgs["wordsI"]
        for wordi in range(len(wordsI)):
            columNum=0
            if purpose == "minRank":
                self.setWordName(wordsI, wordi, columNum); columNum += 1
                self.setRank(wordsI, wordi, columNum); columNum += 1
                self.setFreq(wordsI, wordi, columNum); columNum += 1
                
            elif purpose == "inAnki" or purpose == "tagList":
                self.setWordName(wordsI, wordi, columNum); columNum += 1
                self.setRank(wordsI, wordi, columNum); columNum += 1
                self.setIvl(wordsI, wordi, columNum); columNum += 1
                self.setFreq(wordsI, wordi, columNum); columNum += 1
                
            elif purpose == "notInAnki":
                self.setWordName(wordsI, wordi, columNum); columNum += 1
                self.setRank(wordsI, wordi, columNum); columNum += 1
                self.setFreq(wordsI, wordi, columNum); columNum += 1
                
            elif purpose == "notInFreq":
                self.setWordName(wordsI, wordi, columNum, purpose="notInFreq"); columNum += 1
                self.setFreq(wordsI, wordi, columNum, purpose="notInFreq"); columNum += 1
                
        return dArgs["stats"]
            
            
            
        
    def setAnkiHits(self, wordsI, wordi, columNum):
        newitem = QTableWidgetItem(str(len(wordsI[wordi][1][1][0]["anki"]["ids"])))
        self.setItem(wordi, columNum, newitem)
    
    def setWordName(self, wordsI, wordi, columNum, purpose=None):
        if purpose=="notInFreq":
            display_string = wordsI[wordi][0]
        else:
            display_string = wordsI[wordi][0]
        
        newitem = QTableWidgetItem(display_string)
        #newitem.setCheckState(Qt.Checked)
        newitem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        if purpose=="notInFreq":
            if display_string in self.notInFreqDb and self.notInFreqDb[display_string]["checked"] == 2:
                newitem.setCheckState(Qt.Checked)
            else:
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
        
        newitem = QTableWidgetItem(display_string)
        self.setItem(wordi, columNum, newitem)
    
    def setIvl(self, wordsI, wordi, columNum):
        newitem = QTableWidgetItem(str(wordsI[wordi][1][1][0]["anki"]["ivl"]))
        self.setItem(wordi, columNum, newitem)

