import praw #PythonRedditApiWrapper
import re #Regular Expressions (RegEx)
from credentials import * #Import reddit app access credentials

##Function to initialise PRAW instance
def initReddit():
    #Credential information sourced from file
    reddit = praw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, username = USER_NAME, password = USER_PASSWORD, user_agent = USER_AGENT )
    return reddit

##Count number of posts
def countPosts(inputName, inputType):
    count = -1

    reddit = initReddit()

    if inputType == 'u':
        user = reddit.redditor(inputName)
        listPost = list(user.submissions.new(limit=None))
        count = len(listPost)
    elif inputType == 'r':
        subreddit = reddit.subreddit(inputName)
        listPost = list(subreddit.submissions.new(limit=None))
        count = len(listPost)
    else:
        print "EXCEPTION_THROWN - SECTION_count"
        print "Invalid inputType value. Expected: [u, r]. Recieved: " + inputType

    return count

#Function to remove Emoji & symbols from string
def simpleString(inputString):
    #Remove Emoji by encodeing in ASCII
    inputString = inputString.encode('ascii', 'ignore').decode('ascii')
    #Use RegExp to remove symbols
    inputString = re.sub(r'[^\w]', ' ', inputString)
    return inputString

#Function to remove successive whitespace
def simpleSpace(inputString):
    inputString = re.sub(' +', ' ',inputString)
    return inputString
    