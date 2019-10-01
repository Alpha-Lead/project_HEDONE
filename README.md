#Project HEDONE#

##Scrape Reddit users for media##


**User Guide:**

Hi, thanks for taking an interest in my code.


This is a simple python app to download all the images from a subreddit or reddit user.


You can provide the list of user names, or subreddit names in one of 3 ways:

1. Through the command line call

2. Throught the interactive intefacce

3. Through a textfile



To get started, we will be running the _code_main.py_ script.



Once the code recieves a target (redditor or subreddit) it will scan the length to return how many posts they have.



You will then be prompted to manually enter where you want to start image scan from. This should be an integer. If you imput is 0, negative, or greater then the number of posts, the code will scan for images in the entire thread.

_Note: Reddit will not allow access to more than the last 995 posts._



After you have entered the starting point, the code will scan the posts in range for linked images. These will then be added to a 'panda dataframe' and the number will be listed.



You will then be prompted whether you want to continue downloading these to the ouput folder.


The code will then download the media to the output folder under the subfolder with the target name. All the images will be titled '(NumberOfPost) - (First100CharsOfText).(fileExtension)'



**Commands**

To see help:

`code_main.py --help`

`code_main.py -h`


To enter interactive mode:

`code_main.py`


To download media from user 'redditor':

`code_main.py -u redditor`


To download media from subreddit 'subreddit'

`code_main.py -u subreddit`


To download media from file 'listOfTargets.txt'

`code_main.py -f listOfTargets`


**Guide for using file input method**

There are some rules about acceptable formatting:

*There must only be one redditor username or subreddit name per line

*Entries must be seperated by a newline character

*Entries must be prefixed by 'u/' for redditors and 'r/' for subreddits.

*Lines that are not to be read must have an '#' at the beginning.

*There can be no blank lines.

*Whitespace and tabs before an entry will be ignored.

*File format must be plaintext parsable (I recommend .txt).