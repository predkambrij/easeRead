import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages")

import nltk, codecs, time, os
import anki

from aqt import mw, dialogs

from aqt.qt import QMainWindow, Qt, QWidget
from aqt.utils import showInfo
import pickle

import window, config
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
        dialogs._dialogs["MyWin"] = [window.Window, None]
        winInst = dialogs.open("MyWin", {"logic":logic, "settings":settings})
        
        

class God:
    def __init__(self):
        pass
    def init(self, fname):
        self.fname = fname

    def scanCards(self, wordsToCram, collection=None, ankiIvl=1):
        if collection == None:
            # if collection is not provided, make it yourself (perhaps for command line support)
            collection = anki.Collection("/home/loj/Anki/english/collection.anki2")
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
            nkeys = mw.col.getNote(card.nid).keys()
            sword = False
            if "Front" in nkeys: # 4k essential
                sword = mw.col.getNote(card.nid)["Front"]
            elif "Back" in nkeys: # oxfort picture dict
                sword = mw.col.getNote(card.nid)["Back"]
            
            if sword != None:
                added = False
                for wordComb in wordsToCram.items():
                    if sword == wordComb[0]:
                        juhuN += 1
                        added = True
                        wordsToCram[wordComb[0]][1][0]["anki"]["ids"].append(cardId)
                        wordsToCram[wordComb[0]][1][0]["anki"]["nids"].append(card.nid)
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
        
    def loadFreq1(self, fname):
        freqText = codecs.open(fname, "rb", encoding="utf-8")
        # build structure
        words = {}
        #self.words_in_freqlist = {}
        rank = 0
        for line in freqText:
            num, word, pos, something= line.split(" ")
            rank += 1
            if words.has_key(word.strip()):
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
            if blMap.has_key(ltoken):
                ltoken = blMap[ltoken][0]
            
            # freq list
            if self.freqList.has_key(ltoken):
                if len(ltoken) > 2:
                    if statistics.has_key(ltoken):
                        statistics[ltoken] += 1
                    else:
                        statistics[ltoken] = 1
            else:
                if len(ltoken) > 2:
                    if notInFreq.has_key(ltoken):
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
        for bword, freq in sorted(statistics.items(), key=lambda x:x[1], reverse=True):
            # select words for cramming (minRank and frequency in the book)
            staW = self.freqList[bword]
            if staW[0]["rank"] <= minRank:
                continue
            
            #prepare key for anki card ids
            staW[0]["anki"]={"ids":[],"ivl":-1, "nids":[]}
            wordsToCram[bword] = [freq, staW]
        
        freqLen = {}
        for word, stat in sorted(wordsToCram.items(), key=lambda x:x[1][0], reverse=True):
            if freqLen.has_key(stat[0]):
                freqLen[stat[0]] += 1
            else:
                freqLen[stat[0]] = 1
        
        
        # how much words do you need to learn that you will know words which appear more than x times?
        freqLen2 = {}
        totalWords = 0
        for frequency, numOfWords in sorted(freqLen.items(), key=lambda x:x[0], reverse=True):
            totalWords += numOfWords
            freqLen2[frequency] = totalWords
        
        stats = {}
        stats["uniqWords"]=len(statistics.items())
        stats["toLearn"]=len(wordsToCram.items())
        #print sorted(freqLen.items(), key=lambda x:x[0], reverse=True)
        stats["freq_numToLearn"]=sorted(freqLen2.items(), key=lambda x:x[0], reverse=True)
        
        return wordsToCram, stats, notInFreq
# strange documentation
# vim /nix/store/77vvyiqsng8gnv7yxr9iw616isqkj210-anki-2.0.31/lib/python2.7/site-packages/anki/cards.py 
#loj@think ~/Downloads $ find -L /nix/store/77vvyiqsng8gnv7yxr9iw616isqkj210-anki-2.0.31/lib/python2.7/site-packages/ -type f| xargs grep -in front | grep -v Bina | less -i
#loj@think ~/Downloads $ vim /nix/store/77vvyiqsng8gnv7yxr9iw616isqkj210-anki-2.0.31/lib/python2.7/site-packages/anki/importing/mnemo.py

