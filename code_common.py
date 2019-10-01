import praw #PythonRedditApiWrapper
import re #Regular Expressions (RegEx)
import os #Used to interact with filesystem
import urllib.request #Library to download image
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
    elif inputType == 'r': ### YET TO GET WORKING ###
        subreddit = reddit.subreddit(inputName)
        listPost = list(subreddit.submissions.new(limit=None))
        count = len(listPost)
    else:
        print ("EXCEPTION_THROWN - SECTION_count")
        print ("Invalid inputType value. Expected: [u, r]. Recieved: " + inputType)

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
    
#Function to download file to path
def downloadFile(filepath, filename, filetype, url):
    #Check if file already exists
    if os.path.isfile(filepath):
            print("Skipped file download (exists): " + filename)
    else:
        #Download file from url and name
        try:
            urllib.request.urlretrieve(url, filename=(filepath+filename+filetype))
            print("File downloaded: " + filename)
        except Exception as e:
            print('EXCEPTION_THROWN - SECTION_download')
            print(e)


#Function to ensure downloaded file ouput directory exists
def buildOutputDir(holderFolder, ouputFolder):
    #Get path to file where python app is
    basePath = os.path.dirname(os.path.realpath(__file__))

    filepath = basePath + '\\' + holderFolder + '\\'
    #Check if filepath already exists
    if os.path.isdir(filepath):
        print('Directory already exists: ' + filepath)
    #Create filepath if it does not exist
    else: 
        print('Directory created: ' + filepath)
        os.mkdir(filepath)

    filepath += ouputFolder + '\\'
    #Check if filepath already exists
    if os.path.isdir(filepath):
        print('Directory already exists: ' + filepath)
    #Create filepath if it does not exist
    else: 
        print('Directory created: ' + filepath)
        os.mkdir(filepath)

    return filepath