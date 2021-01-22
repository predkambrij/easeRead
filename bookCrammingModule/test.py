

#from . import window, config, god
import textProcessor, config

settings = {
                    "book_text":config.Config.book_text,
                    "freqCVS":config.Config.freqCVS,
                    "blacklisted_text":config.Config.blacklisted,
                    "blacklisted_man_text":config.Config.blacklisted_man,
                    "hashTag":config.Config.hashTag,
                    "dictDeckName":config.Config.dictDeckName,
                    "notInFreqDb":config.Config.notInFreqDb,
                    }

logic = textProcessor.TextProcessor(settings)

wordsToCram, notInFreq, stats = logic.run(minRank=2500)

print("a "+str(logic.prepareToLearn1(wordsToCram, 1)))
print("a "+str(logic.prepareToLearn1(wordsToCram, 2)))
print("a "+str(logic.prepareToLearn1(wordsToCram, 3)))
pass
