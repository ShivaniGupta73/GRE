import pandas as pd
import msvcrt
import time
from tabulate import tabulate
from os import system

def readch():
    """ Get a single character on Windows.

    see https://docs.microsoft.com/en-us/cpp/c-runtime-library/reference/getch-getwch?view=vs-2019
    """
    ch = msvcrt.getch()
    if ch in b'\x00\xe0':  # Arrow or function key prefix?
        ch = msvcrt.getch()  # Second call returns the actual key code.
    return ch

def addReviewWord(newWord,  meaning, df_review):
    if newWord.lower() not in df_review['Review words'].values:
        df1 = {'Review words': newWord.lower(), 'Review words meaning': meaning}
        df_review = df_review.append(df1, ignore_index = True)
        df_review.to_csv("MyGreReview.csv", index=False)
        print(" Done :) \n")
    else:
        print("Word already present")

def addWordToLearnedWords(word, df_review, df_learned):
    if word.lower() in df_review['Review words'].values and word.lower() not in df_learned['Learned words'].values:
        meaning = df_review[df_review['Review words']==word.lower()]['Review words meaning'].values[0]
        df1 = {'Learned words': word.lower(), 'Learned words meaning': meaning}
        df_learned = df_learned.append(df1, ignore_index = True)
        df_learned.to_csv("MyGreLearned.csv", index=False)
        df_review.drop(df_review.index[(df_review["Review words"] == word.lower())],axis=0,inplace=True)
        df_review.to_csv("MyGreReview.csv", index=False)
        print(" Done :) \n")
    else:
        print("Word not present in review words")

def addLearnedWords(newWord,  meaning, df_learned):
    if newWord.lower() not in df_learned['Learned words'].values:
        df1 = {'Learned words': newWord.lower(), 'Learned words meaning': meaning}
        df_learned = df_learned.append(df1, ignore_index = True)
        df_learned.to_csv("MyGreLearned.csv", index=False)
        print(" Done :) \n")
    else:
        print("Word already present")

def getAllReviewWords(character, df_review):
    print( "\t Word \t Meaning")
    for reviewWords in df_review['Review words']:
        if reviewWords.startswith(character.lower()):
            print("\t", reviewWords, "\t", df_review[df_review['Review words']==reviewWords]['Review words meaning'].values[0])

def getAllLearnedWords(character, df_learned):
    print( "\t Word \t\t Meaning")
    for learnedWords in df_learned['Learned words']:
        if learnedWords.startswith(character.lower()):
            print("\t", learnedWords, "\t", df_learned[df_learned['Learned words']==learnedWords]['Learned words meaning'].values[0])


def getAllReviewWordsWithMeaning(df_review):
    print(tabulate(df_review, headers='keys', tablefmt='psql'))

def getAllLearnedWordsWithMeaning(df_learned):
    print(tabulate(df_learned, headers='keys', tablefmt='psql'))

def flashCardsReviewWords(df_review):
    while True:
        word = df_review.sample()
        print("\n\t\t Word: ",word["Review words"].values[0])
        inword = input(" ")
        print("\t\t Meaning: ",word["Review words meaning"].values[0])
        print("\n**************************************************************","\n")
        key = ord(readch())
        if key == 27:  # Escape key?
            break
        _ = system('cls')
        time.sleep(0.1)

def flashCardsLearnedWords(df_learned):
    while True:
        word = df_learned.sample()
        print("\n\t\t Word: ",word["Learned words"].values[0])
        inword = input(" ")
        print("\t\t Meaning: ",word["Learned words meaning"].values[0])
        print("\n***************************************************************","\n")
        key = ord(readch())
        if key == 27:  # Escape key?
            break
        _ = system('cls')
        time.sleep(0.1)

def deleteWordFromReviewWords(word, df_review):
    if word.lower() in df_review['Review words'].values:
        df_review.drop(df_review.index[(df_review["Review words"] == word.lower())],axis=0,inplace=True)
        df_review.to_csv("MyGreReview.csv", index=False)
        print("\t Done :)")
        print("\t Press enter to go back to the previous menu")
    else:
        print(" Word not present ")
        print("\t Press enter to go back to the previous menu")

def deleteWordFromLearnedWords(word, df_learned):
    if word.lower() in df_learned['Learned words'].values:
        df_learned.drop(df_learned.index[(df_learned["Learned words"] == word.lower())],axis=0,inplace=True)
        df_learned.to_csv("MyGreLearned.csv", index=False)
        print("\t Done :)")
        print("\t Press enter to go back to the previous menu")
    else:
        print(" Word not present ")
        print("\t Press enter to go back to the previous menu")

def searchWord(word,df_review,df_learned):
    if word.lower() in df_review['Review words'].values:
        print("\t" ,word, " : ", df_review[df_review['Review words']==word.lower()]['Review words meaning'].values[0])
    elif word.lower() in df_learned['Learned words'].values:
        print("\t", word, " : ", df_learned[df_learned['Learned words']==word.lower()]['Learned words meaning'].values[0])
    else:
        print("\t Word entered is not present.")

def showTotalNumberOfWords(df_review, df_learned):
    print("\t\t Number of words to review: ",  len(df_review["Review words"]), "\n\t\t Number of words learned: ",
        len(df_learned["Learned words"]), "\n\n\t\t Great job keep learning :)")

def main():
    '''data = {'Review words': [],
        'Review words meaning': [],
        'Learned words': [],
        'Learned words meaning': []}'''

    while True:
        df_review = pd.read_csv("C:\\Users\\Shivani\\Desktop\\python\\GRE\\MyGreReview.csv")
        df_learned = pd.read_csv("C:\\Users\\Shivani\\Desktop\\python\\GRE\\MyGreLearned.csv")

        print("""
            **************Your GRE app: *****************
            Please select an option from the following:
            1. Add a new review word
            2. Add a word from review words to learned words
            3. Add a word to learned words
            4. Get all words from review words for a specific character
            5. Get all words from learned words for a specific character
            6. Show all review words with meaning
            7. Show all learned words with meaning
            8. Flashcards - review words
            9. Flashcards - learned words
            10. Delete word from review words
            11. Delete word from learned words
            12. Look for a word
            13. Show total number of words """)

        select = int(input("\n Please select: "))

        if(select == 1):
            newWord = input("\n Enter new word: ")
            meaning = input("\n Enter meaning of the word: ")
            addReviewWord(newWord,  meaning, df_review)
        elif select == 2:
            word = input("\n Enter word: ")
            addWordToLearnedWords(word, df_review, df_learned)
        elif select == 3:
            word = input("\n Enter learned word: ")
            meaning = input("\n Enter meaning of the word: ")
            addLearnedWords(word,meaning, df_learned)
        elif select == 4:
            character = input("\n Enter character: ")
            getAllReviewWords(character, df_review)
        elif select == 5:
            character = input("\n Enter character: ")
            getAllLearnedWords(character, df_learned)
        elif select == 6:
            getAllReviewWordsWithMeaning(df_review)
        elif select == 7:
            getAllLearnedWordsWithMeaning(df_learned)
        elif select == 8:
            flashCardsReviewWords(df_review)
        elif select == 9:
            flashCardsLearnedWords(df_learned)
        elif select == 10:
            word = input("\n Enter word to be deleted: ")
            deleteWordFromReviewWords(word, df_review)
        elif select == 11:
            word = input("\n Enter word to be deleted: ")
            deleteWordFromLearnedWords(word, df_learned)
        elif select == 12:
            word = input("\n Enter word : ")
            searchWord(word,df_review,df_learned)
        elif select == 13:
            showTotalNumberOfWords(df_review, df_learned)
        else:
            print("Unknown option selected")
        key = ord(readch())
        if key == 27:  # Escape key?
            break
        time.sleep(0.1)

if __name__ == "__main__":
    main()
