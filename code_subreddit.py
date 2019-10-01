#project_HEDONE
import praw #PythonRedditApiWrapper
import urllib #Library to download image
import re #Regular Expressions (RegEx)
import datetime  #Work with Dates
import pandas #To work with dataframes

#Custom function import
from code_common import initReddit, countPosts, simpleString, simpleSpace, downloadFile, buildOutputDir 

def code_subreddit(subredditName):
    #########################################################################
    ##                      Pull data from Reddit                          ##
    #########################################################################

    #Initialise PRAW instance
    reddit = initReddit()

    #Count total number of posts
    print("Counting posts in r/"+subredditName+"...")
    ttlNumPosts = countPosts(subredditName, 'r')
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

    print("Scanning contents of r/"+subredditName+"...")
    #Build object for search - SUBREDDIT
    subreddit = reddit.subreddit(subredditName)
    if searchLimit > 0:
        newPosts = subreddit.new(limit=searchLimit)
    else:
        newPosts = subreddit.new()



    #########################################################################
    ##                       Transform list data                           ##
    #########################################################################

    #Get items from list, export into pandas dataframe object
    postsDF = pandas.DataFrame({"title":[], "body":[], "date":[], "url":[]})
    for submission in newPosts:
        postsDF = postsDF.append(
            {"title": submission.title,
            "body": submission.selftext,
            "date": datetime.datetime.fromtimestamp(submission.created),
            "url": submission.url}, ignore_index=True)

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
    #print(foundDF)
    #print(postsDF) #Whole list, output will crop to only show index & url
    #print(postsDF.loc[0]) #Row 1
    print(str(len(foundDF.index))  + " valid media entries found.")


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



 
 
