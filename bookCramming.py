
import time

# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
import bookCrammingModule



# PYTHONPATH=$PYTHONPATH:/home/loj/.nix-profile/lib/python2.7/site-packages/
# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    ##cardCount = mw.col.cardCount()
    # show a message box
    ##showInfo("Card count: %d" % cardCount)
    
    
    start = time.time()
    
    # just for testing, that I don't have to stop and start Anki each time
    reload(bookCrammingModule) # TODO
    
    bookCrammingModule.BookCrammingModule.run()
    print "seconds %.2f" % (time.time()-start)

    

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

