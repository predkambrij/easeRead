import os

class Config:
    pref =  os.path.dirname(__file__)
    book_text = pref+"/res/book.txt"
    freqCVS = pref+"/res/freq.csv"
    hashTag = "bCram"
    dictDeckName = "book - bCram generated"
    
    # user unchecked word not listed in freq list (eg. Names, acronyms, ...)
    notInFreqDb = pref+"/res/db.notInFreq"
    
    
    
    
