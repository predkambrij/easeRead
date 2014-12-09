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
    print "seconds %.2f" % (time.time()-start)

    

# create a new menu item, "test"
action = QAction("Cramming a Book Vocabulary", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), bookCramming)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

