#project_HEDONE
#Import dependancies
import praw #PythonRedditApiWrapper
import datetime  #Work with Dates
import pandas #To work with dataframes
import os #Used to get directory fro python script

#Custom function import
from code_common import initReddit, countPosts, simpleString, simpleSpace, downloadFile, buildOutputDir, exportDFtoCSV, testUrlCompadible

def code_user(redditorName, csvQuery, lastNum):
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
    if (lastNum < 0):
        while True: #Loop until a valid number is given
            lastPostNum = input("Enter number of last downloaded post: ")
            if( lastPostNum.isdigit() ):
                #Set the search limit (reverse chronological due to 'new' ordering)
                searchLimit = ttlNumPosts - int(lastPostNum)
                break
            else:
                print("Input is not an integer, or <0.\nTry again.")
    else:
        searchLimit = ttlNumPosts - int(lastNum)

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

    #Refine lists with valid media urls, or where the url can be transformed into a valid media url
    foundDF = pandas.DataFrame({"filename":[], "url":[], "extension": []})
    rejectedDF = pandas.DataFrame({"filename":[], "url":[]})
    for i in range(0, len(postsDF.index)):
        test, varStr = testUrlCompadible(postsDF.at[i, 'url'])
        if test == True:
            #Add title, extension, and url to dataframe
            foundDF = foundDF.append({
                "filename": str(ttlNumPosts-i)+' - '+
                                simpleSpace(simpleString(postsDF.at[i, 'title'])).strip(),
                #Filename: <index> - <title -padding (ASCII encoded)>
                "url": varStr,
                "extension": '.'+varStr.split('.')[-1]
            }, ignore_index=True)
        else:
            #Add to exception list
            rejectedDF = rejectedDF.append({
                "filename": str(ttlNumPosts-i)+' - '+
                                simpleSpace(simpleString(postsDF.at[i, 'title'])).strip(),
                #Filename: <index> - <title -padding (ASCII encoded)>
                "url": varStr}, ignore_index=True)

    #Print dataframe contents for debuging
    #print(foundDF) #List with valid download links
    #print(postsDF) #Whole list, output will crop to only show index & url
    #print(postsDF.loc[0]) #Row 1
    print(str(len(foundDF.index)) + " valid media entries found.")


    #########################################################################
    ##                       Export files to CSV                           ##
    #########################################################################

    #Ask if user want's to export post lists
    if csvQuery == True:
        print("Beginning CSV export...")
        outputFilePath = buildOutputDir('output files', redditorName)
        #Export dataframe 'postsDF' to a '.csv' file called 'posts' under redditor output directory,
        exportDFtoCSV(outputFilePath, "posts", postsDF)
        exportDFtoCSV(outputFilePath, "media", foundDF)
        exportDFtoCSV(outputFilePath, "rejected", rejectedDF)
        

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
                return
    #Build filepath
    outputFilePath = buildOutputDir('output files', redditorName)

    #Run download script
    for i in range(0, len(foundDF.index)):
        downloadFile(
                    outputFilePath, #Filepath
                    foundDF.at[i, 'filename'], #Filename
                    foundDF.at[i, 'extension'], #File extension
                    foundDF.at[i, 'url']) #File location URL