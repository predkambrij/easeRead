import anki
from aqt import mw

class AnkiFuncs:
    def __init__(self, settings):
        self.settings = settings

    def templateBack(self, word):
        back = (("<a href='http://www.oxforddictionaries.com/definition/english/%s'>Oxford</a>" % word.replace(" ", "-"))+
            ("&nbsp;&nbsp;<a href='http://dictionary.cambridge.org/dictionary/british/%s'>Cambridge</a>" % word.replace(" ", "-"))+
            ("&nbsp;&nbsp;<a href='https://en.pons.com/translate/english-slovenian/%s'>Pons</a>" % word.replace(" ", "-")) +
            ("&nbsp;&nbsp;<a href='https://www.google.com/search?tbm=isch&q=%s'>Images</a>" % word))
        return back

    def setDefinitions(self, listOfWords):
        deckId = mw.col.decks.id(self.settings["dictDeckName"])
        notes = self.getDeckNotes()
        statistics = {"updated": 0, "added": 0, "refreshed": 0}
        for word in listOfWords:
            res = self.addOrUpdateWord(deckId, notes, word)
            statistics["updated"] += res["updated"]
            statistics["added"] += res["added"]

        res = self.addOrUpdateWord(deckId, notes, updateAll=True)
        statistics["refreshed"] += res["refreshed"]
        return statistics

    def getDeckNotes(self):
        ft = anki.find.Finder(self.settings["collection"])
        notesIDs = ft.findNotes('deck:"%s"' % self.settings["dictDeckName"])
        return [mw.col.getNote(noteId) for noteId in notesIDs]

    def addOrUpdateWord(self, deckId, notes, word=None, updateAll=False):
        statistics = {"updated": 0, "added": 0, "refreshed": 0}
        for note in notes:
            if updateAll == True:
                note["Back"] = self.templateBack(note["Front"])
                statistics["refreshed"] += 1
                note.flush()
            else:
                if note["Front"] == word:
                    note["Back"] = self.templateBack(note["Front"])
                    note.flush()
                    statistics["updated"] += 1
                    return statistics

        if updateAll == True:
            return statistics

        # it's not in collection yet, let's add it then
        note = mw.col.newNote()
        note["Front"] = word
        note["Back"] = self.templateBack(note["Front"])
        note.model()['did'] = deckId
        cards = mw.col.addNote(note)
        statistics["added"] += 1
        return statistics

    def tagWords(self, wordList):
        ankiNoteIds = set([])
        for word in wordList:
            ankiNoteIds |= set(word[1][1][0]["anki"]["nids"])
        self.settings["collection"].tags.bulkAdd(list(ankiNoteIds), self.settings["hashTag"])
        return

    def untagWords(self):
        ft = anki.find.Finder(self.settings["collection"])
        cardIds = ft.findCards("tag:%s" % self.settings["hashTag"])
        ankiNoteIds = set([])
        for cardId in cardIds:
            card = mw.col.getCard(cardId)
            ankiNoteIds.add(card.nid)
        self.settings["collection"].tags.bulkRem(list(ankiNoteIds), self.settings["hashTag"])
