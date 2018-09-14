import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

positiveCommentsList = [] # global list created for positive comments
negativeCommentsList = [] # global list created for negative comments
neutralCommentsList = [] # global list created for neutral comments

negCounter = 0 #the following counters are for the access of the oldest, oldest positive, oldest negative, and oldest neutral comments
posCounter = 0
neutralCounter = 0
oldestCounter = 0

reddit = praw.Reddit(client_id='8DCDH46KmQtMag',
                     client_secret='rUCkKBeCjLW_T25cOow1LOe6Gpg',
                     user_agent='rabblerouzzzer'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comment_sort = 'old' ## this pre-sorts the data from oldest to newest before importing them as submission, as read on PRAW docs
    submission.comments.replace_more(limit=0)

    return submission.comments

def process_comments(comms):
    for i in range(len(comms)):  # a for loop is still required in this method, in order to traverse list comment[indices]
        negScore = get_text_negative_proba(comms[i].body) # this produces a negative score index for comment at index i
        posScore = get_text_positive_proba(comms[i].body) # this produces positive score index for comment at index i
        neuScore = get_text_neutral_proba(comms[i].body) # this produces a neutral score index for comment at index i

        if negScore > posScore and negScore > neuScore: # compares negative value to other values, and appends to negative list if greatest
            negativeCommentsList.append(comms[i].body)
        if posScore > negScore and posScore > neuScore: # compares positive value to other values, and appends to positive list if greatest
            positiveCommentsList.append(comms[i].body)
        if neuScore > negScore and neuScore > posScore: # compares neutral value to other values, and appends to neutral list if greatest
            neutralCommentsList.append(comms[i].body)

        if comms[i].replies != None: # ensures that the list of replies at each comment[i] index is not null
            process_comments(comms[i].replies) # recursive method. Calls method, but with the replies at index comment[i]


def display_list(list): # method displays list contents for positive, negative, and neutral lists, as they are no longer multi-dimensional
    for i in range(len(list)):
        print(list[i])

    print("\n")

def display_oldest_negative(): # method display oldest negative comment from negative comment list, and updates global counter to avoid duplication
    global negCounter
    print("\n\nThe oldest NEGATIVE comment in the thread is: ") # try-catch in case list is empty
    print("=============================================")
    try:
        print(negativeCommentsList[negCounter])  # since sorted at import, oldest negative comment is at index 0
    except:
        print("No values in negative comments list :( ")

    negCounter += 1

def display_oldest_positive(): #method displays oldest positive comment from positive comment list and updates global counter
    global posCounter
    print("\n\nThe oldest POSITIVE comment in the thread is: ")
    print("=============================================")
    try:
        print(positiveCommentsList[posCounter])  # since sorted at import, oldest positive comment is at index 0
    except:
        print("No values in positive comments list :( ")

    posCounter += 1

def display_oldest_neutral(): # displays oldest netural comment from neutral comment list and updates global counter
    global neutralCounter
    print("\n\nThe oldest NEUTRAL comment in the thread is: ")
    print("============================================")
    try:
        print(neutralCommentsList[neutralCounter])  # since sorted at import, oldest neutral comment is at index 0
    except:
        print("No values in neutral comments list :( ")

    neutralCounter += 1


def main():


    global oldestCounter

    userUrl = str(input("\n\nPlease provide the URL for analysis: ")) # allows user to provide URL for analysis
    comments = get_submission_comments(userUrl)

    process_comments(comments)


    print("\nPlease make a selection: ")  # makeshift switch case
    while True:
        userChoice = int(input("\n1) See Positive Comments\n2) See Negative Comments\n3) See Neutral Comments\n4) See Oldest Comment\n5) See Oldest Negative\n6) See Oldest Positive\n7) See Oldest Neutral\n8) Exit\n"))
        if userChoice == 1:
            print("\nPOSITIVE COMMENTS LIST:")
            print("========================")
            display_list(positiveCommentsList)
        elif userChoice == 2:
            print("\nNEGATIVE COMMENTS LIST: ")
            print("========================")
            display_list(negativeCommentsList)
        elif userChoice == 3:
            print("\nNEUTRAL COMMENTS LIST: ")
            print("========================")
            display_list(neutralCommentsList)
        elif userChoice == 4:
            global oldestCounter
            print("\nThe oldest comment in the thread is: ")
            print("=====================================")
            print(comments[oldestCounter].body)
            oldestCounter += 1
        elif userChoice == 5:
            display_oldest_negative()
        elif userChoice == 6:
            display_oldest_positive()
        elif userChoice == 7:
            display_oldest_neutral()
        elif userChoice == 8:
            print("Goodbye!")
            break
        else:
            print("Invalid Selection. GoodBye! ")

            if userChoice == 8: # iterates until user exits
                break

main()
