from importlib import reload
import sys
sys.path.append("/usr/share/anki/")

import nltk, codecs, time, os
import anki

from aqt import mw, dialogs

from aqt.qt import QMainWindow, Qt, QWidget
from aqt.utils import showInfo
import pickle

try:
    from . import window, config
except:
    import window, config

reload(window)
reload(config)


class TextProcessor:
    def __init__(self, settings):
        self.settings = settings

    def run(self, minRank):
        # calculate statistics of words in the book (known in top 5k req list)
        text = codecs.open(self.settings["book_text"], "rb", encoding="utf-8").read()
        freqList = self.loadFreq2(codecs.open(self.settings["freqCVS"], "rb", encoding="utf-8"))
        inFreq, notInFreq = self.countWords(text, freqList)

        # let's check the statistics
        wordsToCram = self.prepareWordsToCram(minRank, freqList, inFreq)

        # how much words do you need to learn that you will know words which appear more than x times?
        freqLen = self.prepareFreqLen(wordsToCram)

        stats = {}
        stats["uniqWords"] = len(list(inFreq.items()))
        stats["toLearn"] = len(list(wordsToCram.items()))
        stats["freq_numToLearn"] = sorted(list(freqLen.items()), key=lambda x: x[0], reverse=True)

        return wordsToCram, notInFreq, stats

    def loadFreq2(self, freqText):
        words = {}
        rank = 0
        for line in freqText:
            word, num = [x.strip() for x in line.split("\t")]
            rank += 1
            if not word in words:
                words[word] = [{"rank": rank}]
        return words

    def countWords(self, text, freqList):
        inFreq = {}
        notInFreq = {}
        tokens = nltk.word_tokenize(text)
        for token in tokens:
            ltoken = token.lower().strip("'").strip("\"").strip(".").strip()

            if len(ltoken) <= 2:
                # too short word
                continue
            if not (ltoken in freqList):
                # match more numbers
                ltoken = ltoken.replace(".", "").replace(",", "")
                try:
                    # omit numbers from not in freq list
                    float(ltoken)
                    continue
                except: pass

            thing = inFreq if (ltoken in freqList) else notInFreq
            if not (ltoken in thing):
                thing[ltoken] = 0
            thing[ltoken] += 1
        return inFreq, notInFreq

    def prepareWordsToCram(self, minRank, freqList, inFreq):
        wordsToCram = {}
        # sort words appeared in book by frequency
        for bword, freq in sorted(list(inFreq.items()), key=lambda x: x[1], reverse=True):
            # select words for cramming (minRank and frequency in the book)
            if freqList[bword][0]["rank"] <= minRank:
                continue
            # prepare key for anki card ids
            details = [{}]
            details[0]["rank"] = freqList[bword][0]["rank"]
            details[0]["anki"] = {"ids": [], "ivl": -1, "nids": []}
            wordsToCram[bword] = [freq, details]
        return wordsToCram

    def prepareFreqLen(self, wordsToCram):
        freqLen = {}
        for word, stat in sorted(list(wordsToCram.items()), key=lambda x: x[1][0], reverse=True):
            if not (stat[0] in freqLen):
                freqLen[stat[0]] = 0
            freqLen[stat[0]] += 1

        freqLen2 = {}
        totalWords = 0
        for frequency, numOfWords in sorted(list(freqLen.items()), key=lambda x: x[0], reverse=True):
            totalWords += numOfWords
            freqLen2[frequency] = totalWords
        return freqLen2

    ###
    def representWords(self, wordsToCram):
        for w in list(wordsToCram.items()):
            if len(w[1][1][0]["anki"]["ids"]) > 0:
                print(w)
                break
        return

    def prepareToLearn(self, stats):
        report = [1, 2, 5, 10]
        reportV = []
        ri = 0
        for t in range(len(stats["freq_numToLearn"]) - 2, -1, -1):
            cond = report[ri] <= stats["freq_numToLearn"][t + 1][0] and report[ri] < stats["freq_numToLearn"][t][0]
            if not cond:
                continue
            reportV.append(stats["freq_numToLearn"][t + 1])
            ri += 1
            if len(report) == ri:
                break
        return reportV

    def prepareToLearn1(self, wordsToCram, minFreq):
        reportV = []
        reportNums = [100, 250, 500]
        wordsI = sorted([x for x in list(wordsToCram.items()) if x[1][0] >= minFreq
                         ], key=lambda x: x[1][1][0]["rank"], reverse=True)
        ri = 0
        for word in wordsI:
            ri += 1
            for reportNum in reportNums:
                if ri == reportNum:
                    reportV.append(tuple([reportNum, word[1][1][0]["rank"]]))

        return reportV