import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

positiveCommentsList = []
negativeCommentsList = []
neutralCommentsList = []

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
    submission.comment_sort = 'old' ## this pre-sorts the data from oldest to newest before importing them as 'submissions'
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


def display_list(list): # method displays list contents for positive, negative, and neutral lists, as they are not multi-dimensional
    for i in range(len(list)):
        print(list[i])

    print("\n")

def main():
    comments = get_submission_comments('https://www.reddit.com/r/worldbuilding/comments/4wbgd1/religions_of_our_current_world_to_show_how/')


    print("\n\nThe oldest comment in the thread is: ")
    print("=====================================")
    print(comments[0].body) # since list is sorted during import, displays first element of list.

    process_comments(comments) # method call arranges all thread comments into the neutral, positive, and negative lists

    print("\n\nThe oldest NEGATIVE comment in the thread is: ")
    print("=============================================")
    try:
        print(negativeCommentsList[0]) # since sorted, oldest negative comment is at index 0
    except:
        print("No values in negative comments list :( ") # in case list is empty


    print("\n\nThe oldest POSITIVE comment in the thread is: ")
    print("=============================================")
    try:
        print(positiveCommentsList[0]) # since sorted, oldest positive comment is at index 0
    except:
        print("No values in positive comments list :( ") # in case list is empty

    print("\n\nThe oldest NEUTRAL comment in the thread is: ")
    print("============================================")
    try:
        print(neutralCommentsList[0]) # since sorted, oldest neutral comment is at index 0
    except:
        print("No values in neutral comments list :( ")




    print("\n\nPOSITIVE COMMENTS LIST:")
    print("========================")
    display_list(positiveCommentsList) # prints positive list

    print("NEUTRAL COMMENTS LIST: ")
    print("========================")
    display_list(neutralCommentsList) # prints neutral lists

    print("NEGATIVE COMMENTS LIST: ")
    print("========================")
    display_list(negativeCommentsList) # prints negative list

main()
