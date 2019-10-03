#project_HEDONE
#Import dependancies
import praw #PythonRedditApiWrapper
import datetime  #Work with Dates
import pandas #To work with dataframes
import os #Used to get directory fro python script

#Custom function import
from code_common import initReddit, countPosts, simpleString, simpleSpace, downloadFile, buildOutputDir, exportDFtoCSV

def code_user(redditorName):
    #########################################################################
    ##                      Pull data from Reddit                          ##
    #########################################################################

    #Initialise PRAW instance
    reddit = initReddit()

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



    #########################################################################
    ##                       Transform list data                           ##
    #########################################################################

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
    #print(foundDF) #List with valid download links
    #print(postsDF) #Whole list, output will crop to only show index & url
    #print(postsDF.loc[0]) #Row 1
    print(str(len(foundDF.index)) + " valid media entries found.")

    #########################################################################
    ##                       Export files to CSV                           ##
    #########################################################################
    #Ask if user want's to download found files
    while True:
        answer = input('Do you want to contiue to export results to csv? [y/n]:')
        if answer.lower().startswith("y"):
            print("Beginning CSV export...")
            outputFilePath = buildOutputDir('output files', redditorName)
            #Export dataframe 'postsDF' to a '.csv' file called 'posts' under redditor output directory,
            exportDFtoCSV(outputFilePath, "posts", postsDF)
        elif answer.lower().startswith("n"):
            break
        

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

    #Build filepath if it does not exist
    if outputFilePath is None:
        outputFilePath = buildOutputDir('output files', redditorName)

    #Run download script
    for i in range(0, len(foundDF.index)):
        downloadFile(
                    outputFilePath, #Filepath
                    foundDF.at[i, 'filename'], #Filename
                    foundDF.at[i, 'extension'], #File extension
                    foundDF.at[i, 'url']) #File location URL