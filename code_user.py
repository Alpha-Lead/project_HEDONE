#project_HEDONE
#Import dependancies
import praw #PythonRedditApiWrapper
import urllib #Library to download image
import datetime  #Work with Dates
import pandas #To work with dataframes
import os #Used to get directory fro python script

#Custom function import
from strManipulators import simpleString, simpleSpace
from redditSetup import initReddit, countPosts

#########################################################################
##                      Pull data from Reddit                          ##
#########################################################################

#Initialise PRAW instance
reddit = initReddit()

#Ask user for input of target name
redditorName = raw_input("Reddit user: u/") #tested with mrCate, Btothensfw, andrewgylb, AcidicSeaYak

#Count total number of posts
print("Counting "+redditorName+"'s posts...")
ttlNumPosts = countPosts(redditorName, 'u')
print ("Total number of posts found: " + str(ttlNumPosts))

#Ask user to limit the number of posts to scan/download based of last download
while True: #Loop until a valid number is given
    lastPostNum = raw_input("Enter number of last downloaded post: ")
    if( lastPostNum.isdigit() ):
        #Set the search limit (reverse chronological due to 'new' ordering)
        searchLimit = ttlNumPosts - int(lastPostNum)
        break
    else:
        print("Input is not an integer, or <0.\nTry again.")

print("Scanning "+redditorName+"'s posts...")
#Build object for search - REDDITOR
redditUsr = reddit.redditor(redditorName)
if searchLimit >0:
    newPosts = redditUsr.submissions.new(limit=searchLimit)
else:
    newPosts = redditUsr.submissions.new()

#Get items from list, export into pandas dataframe object
postsDF = pandas.DataFrame({"title":[], "body":[], "date":[], "url":[], "subreddit":[]})
for submission in newPosts:
    postsDF = postsDF.append(
        {"title": submission.title,
         "body": submission.selftext,
         "date": datetime.datetime.fromtimestamp(submission.created),
         "url": submission.url,
         "subreddit": submission.subreddit}, ignore_index=True)

#Extract all the ones with valid media for a url
extList = ['.jpg', '.png', '.gif', '.mp4', '.jpeg']
foundDF = pandas.DataFrame({"filename":[], "url":[], "extension": []})
for i in range(0, len(postsDF.index)):
   if (postsDF.at[i, 'url']).endswith(tuple(extList)):
        #Add title, extension, and url to dataframe
        foundDF = foundDF.append({
            "filename": str(ttlNumPosts-i)+' - '+
                            simpleSpace(simpleString(postsDF.at[i, 'title'])).strip(),
            #Filename: <index> - <title -padding (ASCII encoded)>
            "url": postsDF.at[i, 'url'],
            "extension": '.'+postsDF.at[i, 'url'].split('.')[-1]
        }, ignore_index=True)

#Print dataframe contents for debuging
print(foundDF)
print(postsDF) #Whole list, output will crop to only show index & url
print(postsDF.loc[0]) #Row 1

###Print Attributes of objects (used for debugging))
##print(dir(redditUsr))
##print(dir(newPosts))


#########################################################################
##                          Download Images                            ##
#########################################################################

#Ask if user want's to download found files #### NEED TO CODE ####
while True:
   answer = raw_input('Do you want to contiue to download phase? [y/n]:')
   if answer.lower().startswith("y"):
      break
   elif answer.lower().startswith("n"):
        print("Exiting on user request...")
        exit()

#Get path to file where python app is
basePath = os.path.dirname(os.path.realpath(__file__))
#Create folder for output from reddit user name
folderPath = '\\redditRipper\\'+redditorName+'\\'

#Create folder if it does not exist
if os.path.isdir(basePath+folderPath):
    print('Directory already exists:' + basePath+folderPath)
else:
    print('Directory created: '+ basePath+folderPath)
    file = os.mkdir(basePath+folderPath)

for i in range(0, len(foundDF.index)):
    try:
        #Build filepath
        filePath=basePath+folderPath
        filePath+=foundDF.at[i, 'filename']
        filePath+=foundDF.at[i, 'extension']

        #Check if file already exists
        if os.path.isfile(filePath):
            print("Skipped file download (exists): " + foundDF.at[i, 'filename'])
        else:
            #Download file from url and name
            urllib.urlretrieve(
                foundDF.at[i, 'url'], 
                filename=filePath)
            print("File downloaded: " + foundDF.at[i, 'filename'])
    except Exception as e:
        print('EXCEPTION_THROWN - SECTION_download')
        print(e)
        #Write to errorLog instead #### NEED TO CODE ####

