from importlib import reload
import sys
#sys.path.append("/usr/local/lib/python2.7/dist-packages")

import nltk, codecs, time, os
import anki

from aqt import mw, dialogs

from aqt.qt import QMainWindow, Qt, QWidget
from aqt.utils import showInfo
import pickle

from . import window, config, textProcessor, ankiFuncs
reload(window)
reload(config)

class BookCrammingModule:
    def __init__(self):
        pass
    
    @classmethod
    def run(cls):
        settings = {"collection":mw.col,
                    "book_text":config.Config.book_text,
                    "freqCVS":config.Config.freqCVS,
                    "hashTag":config.Config.hashTag,
                    "dictDeckName":config.Config.dictDeckName}
        # make an instance of logic class
        textLogic = textProcessor.TextProcessor(settings)
        ankiLogic = ankiFuncs.AnkiFuncs(settings)
        # render a dialog window
        wobj = [window.Window, None]
        dialogs._dialogs["MyWin"] = wobj
        winInst = dialogs.open("MyWin", {"ankiLogic":ankiLogic, "textLogic":textLogic, "settings":settings, "my_window":wobj})

# strange documentation
# vim /usr/share/anki/anki/cards.py
# find -L /usr/share/anki/ -type f| xargs grep -in front | grep -v Bina | less -i
# $ vim /usr/share/anki/anki/importing/mnemo.py

import time

# import the main window object (mw) from ankiqt

# import the "show info" tool from utils.py
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


