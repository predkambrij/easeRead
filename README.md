# Anki addon for building your vocabulary used in specific book

### Getting started
* run `./gen_dot_env.sh` and `./gen_res_files.sh`
* docker-compose build anki2
* copy text for cramming to res/book.txt
* docker-compose up anki2

### Basic usage
* You should see GUI. Choose the language.
* To use this addon click Tools -> Cramming a Book Vocabulary menu
* Adjust "Set rank", "Set freq" and "Min Anki ivl"
* Click "Not in Anki"
* Click "Set Definitions"
* Click "Tag with #bCram"
* Close the window, click "Decks" to refresh the list. You should see "book - bCram generated"
* You can create filtered deck for reviewing. Click Tools -> Create Filtered Deck
* set the filter "tag:bCram" and deselect "Reschedule cards"
* That's the basic usage :) For more details see the following screenshots.


# Screenshots with descriptions
## Default screen
![Image](../master/docImages/default.png?raw=true)

Description of the fields:
* Set rank - select words which have "that" or higher rank (most frequent words in language of the book according by CrammingModule/res/freq.csv)
* Set freq - select words which occur in the book "that" or more times
* Min anki ivl - select cards in Anki which have interval level lower than "that" (that defines words you know or not yet)
* To learn (freq:num) - output which helps you to define proper rank and freq. Second number of each list item means how many words you need to learn if you want to understand all of the words which occurs X or more times. X is the first number of each list item.


## Min Rank
![Image](../master/docImages/minRank.png?raw=true)

Get list of words from book sorted by rank starting from "Set rank" and number of occurance (starting from "Set freq" - Frequency column)

## In Anki
![Image](../master/docImages/inAnki.png?raw=true)

Get list of words from book sorted by rank starting from "Set rank" and number of occurance (starting from "Set freq" - Frequency column).
That list doesn't include words which aren't in Anki.

## Tag words in Anki
![Image](../master/docImages/tagWith.png?raw=true)

Will tag all cards according to the filter with (currently hardcoded) "bCram". The list is the same as provided by "In Anki".
Note: that operaton will delete "bCram" tag from all other cards.

## Untag tagged words
![Image](../master/docImages/unTag.png?raw=true)

Will delete "bCram" tag from all cards.

## Not in Anki
![Image](../master/docImages/notInAnki.png?raw=true)

Will show list of words which aren't in Anki. You can review it and add words manually.

## Generate cards which aren't present in Anki yet
![Image](../master/docImages/defini.png?raw=true)

If you click "Set Definitions" after "Not in Anki", cards you selected (checkbox) will be added in (currently hardcoded) deck "book - bCram generated".
If the template for back side of card was altered, cards will be updated with that operation (that affect just look, interval for cramming won't be changed).

## Generated card example
![Image](../master/docImages/genCard.png?raw=true)

If you click on link, it will open a new tab in your default browser with link (example for Oxford Dictionaries) http://www.oxforddictionaries.com/definition/english/wooden

### Create a Filtered Deck
After you tagged words in "In Anki" list you can create Filtered Deck which will include cards for that list.

## Step 1
![Image](../master/docImages/filtered1.png?raw=true)

## Step 2
![Image](../master/docImages/filtered2.png?raw=true)

Set Search and deselect "Reschedule cards" - that enables you to Rebuild a Filtered Deck multiple times (you can go through deck multiple times).

## Step 3
![Image](../master/docImages/filtered3.png?raw=true)

After you created a Filtered Deck you can rename it to something meaningful.

## Step 4
![Image](../master/docImages/filtered4.png?raw=true)


## Step 5
![Image](../master/docImages/filtered5.png?raw=true)

Here you are. You can study and when you completed simple click Rebuild and you can start again if you want.


### Behind the scenes: How does it work?
* This software requires list of most frequent words in language used in a book (currently hardcoded for English).
The included list (res/freq.csv) was copied from http://www.wordfrequency.info.
* The software will check for book at location res/book.txt

Processing procedure:
* book.txt will be tokenized and each word will be checked for frequecy of occurance and rank according of freq.csv.
* You can set thresholds "Min Rank" (how big is your current vocabulary) and minimum number of occurance of each word. After that you can check the list of words from book starting from rank you specified.
* You can check which words according of your filter are present in Anki (import great shared decks from https://ankiweb.net/shared/decks/) - the software searches for pattern of used in 4000 Essential English and Oxford Picture Dictionary).
* Tag words according of your filter with (currently hardcoded) "bCram" - that enable you to make Filtered Deck.

TODOs / known issues:
* it wasn't tested on other platform than Linux Mint yet
* some actions (In Anki, Not in Anki) may take quite a lot of time (up to half of minute if you have 30000 cards) - it should be progress bar or optimized
* field "To learn" doesn't consider known words in Anki yet (just information showing - "Tag with #bCram" button won't tag words you know)
* try to consider part of speach of each word or phrase (like "looking for", "is working") for normalization ("is working" -> work; don't split "looking for")
* try to get better coverage of words in a book (they are lost during checking with most frequent words because they aren't normalized)
* if you want to generate cards which aren't exist in Anki yet, you have to create deck "book - bCram generated" in advance
