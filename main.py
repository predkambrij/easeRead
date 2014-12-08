import nltk, codecs, time


class God:
    def __init__(self, fname):
        self.fname = fname
        pass
    def load(self):
        return codecs.open(self.fname, "rb", encoding="utf-8").read()
    def loadFreq(self, fname):
        """
        fname in CSV format
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
        
        print len(statistics.items())
        print len(wordsToCram.items())
        print sorted(freqLen.items(), key=lambda x:x[0], reverse=True)
        print sorted(freqLen2.items(), key=lambda x:x[0], reverse=True)
        
        # print sample words which starts from minRank
        for sta in sorted(wordsToCram.items(), key=lambda x:x[1][1][0]["rank"], reverse=False)[:30]:
            print sta
        

if __name__ == "__main__":
    start = time.time()
    g = God("/home/loj/Downloads/Far_From_The_Madding_Crowd-Thomas_Hardy.txt")
    g.loadFreq("/home/loj/Downloads/freq.csv")
    g.run()
    print "seconds %.2f" % (time.time()-start)
    
    print "end"
