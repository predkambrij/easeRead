#Anki addon for building your vocabulary used in specific book

###How does it work?
* This software requires list of most frequent words in language used in a book (currently hardcoded for English).
The included list (bookCrammingModule/res/freq.csv) was copied from http://www.wordfrequency.info.
* The software will check for book at location bookCrammingModule/res/book.txt

Processing procedure:
* book.txt will be tokenized and each word will be checked for frequecy of occurance and rank according of freq.csv.
* You can set thresholds "Min Rank" (how big is your current vocabulary) and minimum number of occurance of each word. After that you can check the list of words from book starting from rank you specified.
* You can check which words according of your filter are present in Anki (import great shared decks from https://ankiweb.net/shared/decks/) - the software searches for pattern of used in 4000 Essential English and Oxford Picture Dictionary).
* Tag words according of your filter with (currently hardcoded) "bCram" - that enable you to make Filtered Deck.

Installation procedure:
* Download ZIP or clone git repository
* copy bookCramming.py and bookCrammingModule to Anki/addons directory and restart Anki
* You can access this addon by Tools -> Cramming a Book Vocabulary menu

TODOs / known issues:
* field "To learn" doesn't consider known words in Anki yet (just information showing - "Tag with #bCram" button won't tag words you know)
* try to use part of speach and definitions from oxford dictionary for words which aren't present in Anki yet
* try to consider part of speach of each word or phrase (like "looking for", "is working") for normalization ("is working" -> work; don't split "looking for")
* try to get better coverage of words in a book (they are lost during checking with most frequent words because they aren't normalized)


#Screenshots with descriptions
##Default screen
![Image](../master/docImages/default.png?raw=true)

Description of the fields:
* Set rank - select words which have "that" or higher rank (most frequent words in language of the book according by CrammingModule/res/freq.csv)
* Set freq - select words which occur in the book "that" or more times
* Min anki ivl - select cards in Anki which have interval level lower than "that" (that defines words you know or not yet)
* To learn (freq:num) - output which helps you to define proper rank and freq. Second number of each list item means how many words you need to learn if you want to understand all of the words which occurs X or more times. X is the first number of each list item.


##Min Rank
![Image](../master/docImages/minRank.png?raw=true)

Get list of words from book sorted by rank starting from "Set rank" and number of occurance (starting from "Set freq" - Frequency column)

##In Anki
![Image](../master/docImages/inAnki.png?raw=true)

Get list of words from book sorted by rank starting from "Set rank" and number of occurance (starting from "Set freq" - Frequency column).
That list doesn't include words which aren't in Anki.

##Tag words in Anki
![Image](../master/docImages/tagWith.png?raw=true)

Will tag all cards according to the filter with (currently hardcoded) "bCram". The list is the same as provided by "In Anki".
Note: that operaton will delete "bCram" tag from all other cards.

##Untag tagged words
![Image](../master/docImages/unTag.png?raw=true)

Will delete "bCram" tag from all cards.

##Not in Anki
![Image](../master/docImages/notInAnki.png?raw=true)

Will show list of words which aren't in Anki. You can review it and add words manually. Next release will most probably include feature to get definition from Oxford dictionary or will provide a link to definition for words you will choose.

###Create a Filtered Deck
After you tagged words in "In Anki" list you can create Filtered Deck which will include cards for that list.

##Step 1
![Image](../master/docImages/filtered1.png?raw=true)

##Step 2
![Image](../master/docImages/filtered2.png?raw=true)

Set Search and deselect "Reschedule cards" - that enables you to Rebuild a Filtered Deck multiple times (you can go through deck multiple times).

##Step 3
![Image](../master/docImages/filtered3.png?raw=true)

After you created a Filtered Deck you can rename it to something meaningful.

##Step 4
![Image](../master/docImages/filtered4.png?raw=true)


##Step 5
![Image](../master/docImages/filtered5.png?raw=true)

Here you are. You can study and when you completed simple click Rebuild and you can start again if you want.


