import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages")

import nltk, codecs, time
import anki

from aqt import mw, dialogs

from aqt.qt import QMainWindow, Qt, QWidget
from aqt.utils import showInfo
import pickle

import window
reload(window)

class BookCrammingModule:
    def __init__(self):
        pass
    
    @classmethod
    def run(cls):
        # collection of all of the cards, filters, everything your heart can imagine
        collection = mw.col
        
        g = God("/home/loj/Downloads/Far_From_The_Madding_Crowd-Thomas_Hardy.txt")
        g.loadFreq("/home/loj/Downloads/freq.csv")
        
        runpickle = 1
        if runpickle == 0:
            wordsToCram, stats = g.run()
            wordsToCram = g.scanCards(wordsToCram, collection, userKnow=False)
            pik = open('/home/loj/wordsToCram.pkl', 'wb')
            pickle.dump(wordsToCram, pik, pickle.HIGHEST_PROTOCOL)
            pik.close()
        else:
            pik = open('/home/loj/wordsToCram.pkl', 'rb')
            wordsToCram = pickle.load(pik)
        
        wordsToCram, stats = g.run()
        
        print g.representWords(wordsToCram)
        print "juhu"
        
        
        dialogs._dialogs["MyWin"] = [window.Window, None]
        winInst = dialogs.open("MyWin")
        winInst.renderTable(wordsToCram)

class God:
    def __init__(self, fname):
        self.fname = fname
        pass


    def scanCards(self, wordsToCram, collection=None, userKnow=True):
        if collection == None:
            # if collection is not provided, make it yourself (perhaps for command line support)
            collection = anki.Collection("/home/loj/Anki/english/collection.anki2")
        ft = anki.find.Finder(collection)
        
        # find all of the cards user know (interval level is bigger than 1 day)
        # and find cards user doesn't know (interval not defined or something)
        if userKnow == True:
            cards = ft.findCards("prop:ivl>1") # cards user knows
        else:
            cards = ft.findCards("prop:ivl<=1") # cards user doesn't know
        
        juhuN = 0
        
        for cardId in cards:
            card = mw.col.getCard(cardId)
            question = card.q()
            answer = card.a()
            nkeys = mw.col.getNote(card.nid).keys()
            sword = False
            if "Front" in nkeys: # 4k essential
                sword = mw.col.getNote(card.nid)["Front"]
            elif "Back" in nkeys: # oxfort picture dict
                sword = mw.col.getNote(card.nid)["Back"]
            
            if sword != None:
                for wordComb in wordsToCram.items():
                    if sword == wordComb[0]:
                        juhuN += 1
                        wordsToCram[wordComb[0]][1][0]["anki"]["ids"].append(cardId)
                        wordsToCram[wordComb[0]][1][0]["anki"]["ivl"]=card.ivl
                        
        print "juhuns",juhuN
        return wordsToCram
    def representWords(self,wordsToCram):
        for w in wordsToCram.items():
            if len(w[1][1][0]["anki"]["ids"]) > 0:
                print w
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
            if words.has_key(word.strip()):
                words[word.strip()].append({"rank":int(rank.strip()), "pos":pos.strip(), "dispersion":float(dispersion.strip())})
            else:
                words[word.strip()] = [{"rank":int(rank.strip()), "pos":pos.strip(), "dispersion":float(dispersion.strip())}]
            # just to speedup search we have redundant dict
            #self.words_in_freqlist[word.strip()] = 1
        self.freqList = words
        
    def run(self):
        text = self.load()
        # tokenize
        tokens = nltk.word_tokenize(text)
        
        # calculate statistics of words in the book (known in top 5k req list)
        statistics = {}
        for token in tokens:
            ltoken = token.lower()
            
            if self.freqList.has_key(ltoken):
                if statistics.has_key(ltoken):
                    statistics[ltoken] += 1
                else:
                    statistics[ltoken] = 1
        
        # let's check the statistics
        minRank = 2500
        wordsToCram = {}
        # sort words appeared in book by frequency
        for bword, freq in sorted(statistics.items(), key=lambda x:x[1], reverse=True):
            # select words for cramming (minRank and frequency in the book)
            staW = self.freqList[bword]
            if staW[0]["rank"] <= minRank:
                continue
            
            #prepare key for anki card ids
            staW[0]["anki"]={"ids":[],"ivl":-1}
            wordsToCram[bword] = [freq, staW]
            
            lim = 0
        lbla = len(wordsToCram.items())
        freqLen = {}
        for word, stat in sorted(wordsToCram.items(), key=lambda x:x[1][0], reverse=True):
            if freqLen.has_key(stat[0]):
                freqLen[stat[0]] += 1
            else:
                freqLen[stat[0]] = 1
            
            
            lim += 1
            if lim < 30:# or (lbla -lim) < 10:
                print word, stat
        
        # how much words do you need to learn that you will know words which appear more than x times?
        freqLen2 = {}
        totalWords = 0
        for frequency, numOfWords in sorted(freqLen.items(), key=lambda x:x[0], reverse=True):
            totalWords += numOfWords
            freqLen2[frequency] = totalWords
        
        stats = {}
        print len(statistics.items())
        print len(wordsToCram.items())
        print sorted(freqLen.items(), key=lambda x:x[0], reverse=True)
        print sorted(freqLen2.items(), key=lambda x:x[0], reverse=True)
        
        # print sample words which starts from minRank
        for sta in sorted(wordsToCram.items(), key=lambda x:x[1][1][0]["rank"], reverse=False)[:30]:
            print sta
        return wordsToCram, stats
# strange documentation
# vim /nix/store/77vvyiqsng8gnv7yxr9iw616isqkj210-anki-2.0.31/lib/python2.7/site-packages/anki/cards.py 
#loj@think ~/Downloads $ find -L /nix/store/77vvyiqsng8gnv7yxr9iw616isqkj210-anki-2.0.31/lib/python2.7/site-packages/ -type f| xargs grep -in front | grep -v Bina | less -i
#loj@think ~/Downloads $ vim /nix/store/77vvyiqsng8gnv7yxr9iw616isqkj210-anki-2.0.31/lib/python2.7/site-packages/anki/importing/mnemo.py

