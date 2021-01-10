from importlib import reload
import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages")

import nltk, codecs, time, os
import anki

from aqt import mw, dialogs

from aqt.qt import QMainWindow, Qt, QWidget
from aqt.utils import showInfo
import pickle

from . import window, config
reload(window)
reload(config)

class BookCrammingModule:
    def __init__(self):
        pass
    
    @classmethod
    def run(cls):
        # settings
        settings = {
                    "collection":mw.col,
                    "book_text":config.Config.book_text,
                    "freqCVS":config.Config.freqCVS,
                    "blacklisted_text":config.Config.blacklisted,
                    "blacklisted_man_text":config.Config.blacklisted_man,
                    "hashTag":config.Config.hashTag,
                    "dictDeckName":config.Config.dictDeckName,
                    "notInFreqDb":config.Config.notInFreqDb,
                    #"notInFreqCambrWCFile":config.Config.notInFreqCambrWC,
                    }
        # make an instance of logic class
        logic = God()
        
        # render a dialog window
        wobj = [window.Window, None]
        dialogs._dialogs["MyWin"] = wobj
        winInst = dialogs.open("MyWin", {"logic":logic, "settings":settings, "my_window":wobj})
        
        

class God:
    def __init__(self):
        pass
    def init(self, fname):
        self.fname = fname

    def scanCards(self, wordsToCram, collection=None, ankiIvl=1):
        if collection == None:
            # if collection is not provided, make it yourself (perhaps for command line support)
            collection = anki.Collection("/home/user/.local/share/Anki2/User 1/collection.anki2")
        ft = anki.find.Finder(collection)
        
        # interval level from where user doesn't know (let's say if it's shorter than 1 day
        if ankiIvl == None:
            cards = ft.findCards("prop:ivl<=%i"%500000)
        else:
            cards = ft.findCards("prop:ivl<=%i"%ankiIvl)
        
        juhuN = 0
        
        for cardId in cards:
            card = mw.col.getCard(cardId)
            #question = card.q()
            #answer = card.a()
            nkeys = list(mw.col.getNote(card.nid).keys())
            sword = False
            if "Front" in nkeys: # 4k essential
                sword = mw.col.getNote(card.nid)["Front"]
            elif "Back" in nkeys: # oxfort picture dict
                sword = mw.col.getNote(card.nid)["Back"]
            
            if sword != None:
                added = False
                for wordComb in list(wordsToCram.items()):
                    if sword == wordComb[0]:
                        juhuN += 1
                        added = True
                        wordsToCram[wordComb[0]][1][0]["anki"]["ids"].append(cardId)
                        wordsToCram[wordComb[0]][1][0]["anki"]["nids"].append(card.nid)
                        wordsToCram[wordComb[0]][1][0]["anki"]["ivl"]=card.ivl
                        
        print("juhuns",juhuN)
        return wordsToCram
    def representWords(self,wordsToCram):
        for w in list(wordsToCram.items()):
            if len(w[1][1][0]["anki"]["ids"]) > 0:
                print(w)
                break
        return
        
        
        # find front or back words that user can select them or one kind of pattern
        
        
        
    
    def load(self):
        return codecs.open(self.fname, "rb", encoding="utf-8").read()
    def loadFreq(self, fname):
        """
        fname in CSV format
        from http://www.wordfrequency.info/top5000.asp
        fields: Rank    Word Part of speech  Frequency       Dispersion
        """
        freqText = codecs.open(fname, "rb", encoding="utf-8")
        
        # build structure
        words = {}
        #self.words_in_freqlist = {}
        for line in freqText:
            rank, word, pos, freq, dispersion = line.split("\t")
            if word.strip() in words:
                words[word.strip()].append({"rank":int(rank.strip()), "pos":pos.strip(), "dispersion":float(dispersion.strip())})
            else:
                words[word.strip()] = [{"rank":int(rank.strip()), "pos":pos.strip(), "dispersion":float(dispersion.strip())}]
            # just to speedup search we have redundant dict
            #self.words_in_freqlist[word.strip()] = 1
        self.freqList = words
        
    def loadFreq1(self, fname):
        freqText = codecs.open(fname, "rb", encoding="utf-8")
        # build structure
        words = {}
        #self.words_in_freqlist = {}
        rank = 0
        for line in freqText:
            numa, worda, _something2, posa, somethinga= line.split("\t")
            num, word, pos, something = numa.strip(), worda.strip(), posa.strip(), somethinga.strip()
            rank += 1
            if word.strip() in words:
                words[word.strip()].append({"rank":rank, "pos":pos.strip()})
            else:
                words[word.strip()] = [{"rank":rank, "pos":pos.strip()}]
            
        self.freqList = words
        return
    
    def run(self, minRank, blMap):
        notInFreq = {}
        text = self.load()
        # tokenize
        tokens = nltk.word_tokenize(text)
        
        # calculate statistics of words in the book (known in top 5k req list)
        statistics = {}
        for token in tokens:
            ltoken = token.lower()
            ltoken = ltoken.strip("'").strip("\"").strip()
            
            # quick 'n' dirty fix for plurals, past verb forms, ..
            if ltoken in blMap:
                ltoken = blMap[ltoken][0]
            
            # freq list
            if ltoken in self.freqList:
                if len(ltoken) > 2:
                    if ltoken in statistics:
                        statistics[ltoken] += 1
                    else:
                        statistics[ltoken] = 1
            else:
                if len(ltoken) > 2:
                    if ltoken in notInFreq:
                        notInFreq[ltoken] += 1
                    else:
                        notInFreq[ltoken] = 1
                
        #codecs.open("/tmp/notIn", "wb", encoding="utf-8").write(
        #                    "\n".join(
        #                              [x[0]+"\t"+unicode(x[1]) for x in sorted(notInFreq.items(),key=lambda x:x[1],reverse=True)]
        #                              )
        #                                      )
        # let's check the statistics
        wordsToCram = {}
        # sort words appeared in book by frequency
        for bword, freq in sorted(list(statistics.items()), key=lambda x:x[1], reverse=True):
            # select words for cramming (minRank and frequency in the book)
            staW = self.freqList[bword]
            if staW[0]["rank"] <= minRank:
                continue
            
            #prepare key for anki card ids
            staW[0]["anki"]={"ids":[],"ivl":-1, "nids":[]}
            wordsToCram[bword] = [freq, staW]
        
        freqLen = {}
        for word, stat in sorted(list(wordsToCram.items()), key=lambda x:x[1][0], reverse=True):
            if stat[0] in freqLen:
                freqLen[stat[0]] += 1
            else:
                freqLen[stat[0]] = 1
        
        
        # how much words do you need to learn that you will know words which appear more than x times?
        freqLen2 = {}
        totalWords = 0
        for frequency, numOfWords in sorted(list(freqLen.items()), key=lambda x:x[0], reverse=True):
            totalWords += numOfWords
            freqLen2[frequency] = totalWords
        
        stats = {}
        stats["uniqWords"]=len(list(statistics.items()))
        stats["toLearn"]=len(list(wordsToCram.items()))
        #print sorted(freqLen.items(), key=lambda x:x[0], reverse=True)
        stats["freq_numToLearn"]=sorted(list(freqLen2.items()), key=lambda x:x[0], reverse=True)
        
        return wordsToCram, stats, notInFreq
# strange documentation
# vim /usr/share/anki/anki/cards.py
# find -L /usr/share/anki/ -type f| xargs grep -in front | grep -v Bina | less -i
# $ vim /usr/share/anki/anki/importing/mnemo.py

import time

# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
import bookCrammingModule



# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def bookCramming():
    # measure how much of the time the function takes
    start = time.time()
    
    # used during development, that I didn't have to stop and start Anki each time
    # it's nothing wrong with that
    reload(bookCrammingModule)
    
    bookCrammingModule.BookCrammingModule.run()
    print("seconds %.2f" % (time.time()-start))

    

# create a new menu item, "test"
action = QAction("Cramming a Book Vocabulary", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(bookCramming)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


