#project_HEDONE
#Import dependancies
import praw #PythonRedditApiWrapper
import datetime  #Work with Dates
import pandas #To work with dataframes
import os #Used to get directory fro python script

#Custom function import
from code_common import *

#########################################################################
##                      Pull data from Reddit                          ##
#########################################################################

#Initialise PRAW instance
reddit = initReddit()

#Ask user for input of target name
redditorName = input("Reddit user: u/")

#Count total number of posts
print("Counting "+redditorName+"'s posts...")
ttlNumPosts = countPosts(redditorName, 'u')
print ("Total number of posts found: " + str(ttlNumPosts))

#Ask user to limit the number of posts to scan/download based of last download
while True: #Loop until a valid number is given
    lastPostNum = input("Enter number of last downloaded post: ")
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
   answer = input('Do you want to contiue to download phase? [y/n]:')
   if answer.lower().startswith("y"):
      break
   elif answer.lower().startswith("n"):
        print("Exiting on user request...")
        exit()

outputFilePath = buildOutputDir('output files', redditorName)

for i in range(0, len(foundDF.index)):
    downloadFile(
                 outputFilePath, #Filepath
                 foundDF.at[i, 'filename'], #Filename
                 foundDF.at[i, 'extension'], #File extension
                 foundDF.at[i, 'url']) #File location URL


