import praw #PythonRedditApiWrapper
import re #Regular Expressions (RegEx)
import os #Used to interact with filesystem
import urllib.request #Library to download image & process html
from bs4 import BeautifulSoup #Library used to parse html content
from credentials import * #Import reddit app access credentials

##Function to print 'Help' script
def printHelp():
    print("Python script to download all media from a reddit user or subreddit.")
    print("1) Command line use:")
    print("   >> code_main.py <flags> <type> <input>")
    print("   Export findings to csv file")
    print("     - Flag: -c --csv")
    print("   Specify the number of the last downloaded file")
    print("     - Flag: -n --from")
    print("     - Must be followed by the integer value of where the search should go from")
    print("     - OR, you can specify to download all. This should not be followed by a specified integer.")
    print("     - Flag: -a --all")
    print("   Download all from list file")
    print("     - Type: -f --file")
    print("     - Input: path to file")
    print("     - Input file entries should be seperated by a newline.")
    print("     - Input file entries shourd be prefixed with 'r/' or 'u/'.")
    print("     - Input file lines begining with '#' will be skipped.")
    print("   Download from reddit user")
    print("     - Type: -u --user")
    print("     - Input: Redditor username")
    print("   Download all from list file")
    print("     - Type: -r --subreddit")
    print("     - Input: Subreddit name")
    print("2) Interactive use:")
    print("   >> code_main.py")
    return

#########################################################################
##                      Reddit functionality                           ##
#########################################################################

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
        listPost = list(subreddit.new(limit=None))
        count = len(listPost)
    else:
        print ("EXCEPTION_THROWN - SECTION_count")
        print ("Invalid inputType value. Expected: [u, r]. Recieved: " + inputType)

    return count

#########################################################################
##                      String simplification                          ##
#########################################################################

#Function to remove Emoji & symbols from string
def simpleString(inputString):
    #Remove Emoji by encodeing in ASCII
    inputString = inputString.encode('ascii', 'ignore').decode('ascii')
    #Use RegExp to remove symbols
    inputString = re.sub(r'[^\w]', ' ', inputString)
    return inputString

#Function to remove successive whitespace
def simpleSpace(inputString):
    #Remove whitespace
    inputString = re.sub(' +', ' ',inputString)
    #Remove tabbing
    inputString = re.sub(r'\t', '',inputString)
    #Limit to 100 characters
    inputString = (inputString[:100] + ' ... ') if len(inputString) > 100 else inputString
    return inputString

#########################################################################
##                  Directory handling  & Downloading                  ##
#########################################################################

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
            print("Url: " + url)
            print("Filename: " + filepath+filename+filetype)
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

#########################################################################
##                       Export files to CSV                           ##
#########################################################################

#Function to dexport Pandas DataFrame to CSV file
def exportDFtoCSV(filepath, filename, dataFrame):
    #Check if file already exists
    if os.path.isfile(filepath+"\\"+filename+".csv"):
            print("Cancelled CSV export. File exists: " + filename + ".csv")
    else:
        #Download file from url and name
        try:
            dataFrame.to_csv (filepath + "\\" + filename + ".csv", index = None, header=True) 
            print("CSV Created: " + filename + ".csv")
        except Exception as e:
            print('EXCEPTION_THROWN - SECTION_export')
            print("FilePath: " + filepath)
            print("Filename: " + filename + ".csv")
            print(e)


#########################################################################
##                      HTML parse & extract                           ##
#########################################################################

#Function to get tag attribute value from html page
# #<tag_search tagTarget=RETURN tag_att_nm='tag_attr_val' />
def extractHtmlAttrArg(url, tag_search, tag_target, tag_attr_nm, tag_attr_val):
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(url)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    # Take out the <div> of name and get its value
    name_box = soup.find(tag_search, attrs={tag_attr_nm: tag_attr_val})
    out = name_box.get(tag_target)
    if isinstance(out, list): 
        return out[1]
    else:
        return out

#<tag_search tagTarget=RETURN />
def extractHtmlAttr(url, tag_search, tag_target): 
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(url)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    # Take out the <div> of name and get its value
    name_box = soup.find(tag_search)
    out = name_box.get(tag_target)
    if isinstance(out, list): 
        print("List ^")
        return out[1]
    else:
        return out

#Function to get tag value from html page
#<tag_search tag_att_nm='tag_attr_val'>RETURN</tag_search>
def extractHtmlValueArg(url, tag_search, tag_attr_nm, tag_attr_val):
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(url)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    # Take out the <div> of name and get its value
    name_box = soup.find(tag_search, attrs={tag_attr_nm: tag_attr_val})
    #Return value between <> </> by stripping the tags off
    return name_box.text.strip()

#<tag_search>RETURN</tag_search>
def extractHtmlValue(url, tag_search):
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(url)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    # Take out the <div> of name and get its value
    name_box = soup.find(tag_search)
    #Return value between <> </> by stripping the tags off
    return name_box.text[1].strip()

#<tag_search>
def checkHtmlTag(url, tag_search):
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(url)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    # Take out the <div> of name and get its value
    name_box = soup.find(tag_search)
    if name_box != None:
        return True
    else:
        return False

#<tag_search tag_att_nm='tag_attr_val'>
def checkHtmlTagArg(url, tag_search, tag_attr_nm, tag_attr_val):
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(url)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    # Take out the <div> of name and get its value
    name_box = soup.find(tag_search, attrs={tag_attr_nm: tag_attr_val})
    if name_box != None:
        return True
    else:
        return False

#########################################################################
##                   Test & transform media url                        ##
#########################################################################

#Function to test if url is not direct media, return test result (and useable url)
def testUrlCompadible(url):
    #Url linkes straight to media, no transformation needed
    extList = ['.jpg', '.png', '.gif', '.mp4', '.jpeg']
    if url.endswith(tuple(extList)):
        return True, url

    #Url needs Gfycat transformation
    elif ("gfycat.com/" in url):
        return True, changeGfycat(url)
    
    #Url needs Imgur transformation
    elif ("imgur.com/" in url):
        return True, changeImgur(url)

    #Url does not meet any conditions, not valid for download
    else:
        return False, url


#Function to change gfycat urls for download
def changeGfycat(url):
    #Convert from '.gifv' to '.gif' if necessary
    if (url.endswith(".gifv")):
        return url[:-1]
    
    #Search page source for link if no other option works
    else:
        #Input url: https://gfycat.com/mediaRefId
        #HTML tag:  <source src="https://giant.gfycat.com/newMediaRefID.mp4" type="video/mp4"/>
        return extractHtmlAttrArg(url, 'source', 'src', 'type', 'video/mp4')

#Function to change i.imgur urls for download
def changeImgur(url):
    if (url.endswith(".gifv")):
        #Remove the final 'v' from url
        return url[:-1]
    else: #Input url: https://gfycat.com/mediaRefId
        #<meta property="og:type" content="video.other" />
        if('video' in extractHtmlAttrArg(url, 'meta', 'content', 'property', 'og:type')): 
            #Check if "property='og:video'" exists
            if (checkHtmlTagArg(url, 'meta', 'property', 'og:video')):
                #Video
                #HTML tag:  <meta property="og:video" content="https://i.imgur.com/newMediaRefID.mp4" />
                return extractHtmlAttrArg(url, 'meta', 'content', 'property', 'og:video')
            else:
                #GIF
                #HTML tag:  <meta property="og:image" content="https://newMediaRefID.gif?noredirect" />
                return extractHtmlAttrArg(url, 'meta', 'content', 'property', 'og:image').rsplit('?', 1)[1]
        #<meta property="og:type" content="article" />
        else: 
            #HTML tag:  <meta property="og:image" content="https://i.imgur.com/newMediaRefID.jpg?fb" />
            return extractHtmlAttrArg(url, 'meta', 'content', 'property', 'og:image').rsplit('?', 1)[1]
