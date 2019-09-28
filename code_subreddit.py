#project_HEDONE
import praw #PythonRedditApiWrapper
import urllib #Library to download image
import re #Regular Expressions (RegEx)
import datetime  #Work with Dates
import pandas #To work with dataframes

#Custom function import
from strManipulators import simpleString, simpleSpace
from redditSetup import initReddit, countPosts

#########################################################################
##                      Pull data from Reddit                          ##
#########################################################################

#Initialise PRAW instance
reddit = initReddit()
searchLimit = 5 #if 0 or -ve, then search all
subredditName = 'HelloInternet'

#Build object for search - SUBREDDIT
subreddit = reddit.subreddit(subredditName)
if searchLimit > 0:
  newPosts = subreddit.new(limit=searchLimit)
else:
 newPosts = subreddit.new()

#Print out
for submission in newPosts:
        #Post title
        varTitle = submission.title
        #Contents of the post, blank if link
        varContent = submission.selftext
        #If post is a link, linked url
        varLinkUrl = submission.url 
        print("Title: {}\nContent: {}\nUrl: {}\n".format(varTitle, varContent, varLinkUrl))

print("\n\n----------\n\n")


###Print Attributes of objectswhen coding
##print(dir(redditUsr))
##print(dir(newPosts))


#########################################################################
##                          Download Images                            ##
#########################################################################

#Ask if user want's to download found files
while True:
   answer = input('Do you want to contiue to download phase? [y/n]:')
   if answer.lower().startswith("y"):
      break
   elif answer.lower().startswith("n"):
        print("Exiting on user request...")
        exit()

outputFilePath = buildOutputDir('output files', subredditName)

for i in range(0, len(foundDF.index)):
    downloadFile(
                 outputFilePath, #Filepath
                 foundDF.at[i, 'filename'], #Filename
                 foundDF.at[i, 'extension'], #File extension
                 foundDF.at[i, 'url']) #File location URL



 
 
