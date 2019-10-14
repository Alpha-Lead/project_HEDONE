#project_HEDONE
#Import dependancies
import sys #To handle passing in arguments
import getopt #To handle argument parsing
import os #Used to interact with filesystem
import re #Used for regex expressions on strings

from code_user import code_user #To operate on users
from code_subreddit import code_subreddit #To operate on subreddits
from code_common import printHelp #Print out help script

##Process arguments
def main(argv):
    try:
        optns, args = getopt.getopt(argv, "f:u:s:h:c", ["file=", "user=", "subreddit=", "help=", "csv"])
    except getopt.GetoptError:
        print("EXCEPTION_THROWN - SECTION_arguments")
        print("Invalid arguments.")
        print("code_main.py <flag> <name/filepath>")
        print("    FLAG       |      DESCRIPTION")
        print("---------------|------------------------------------")
        print("-f --file      | Input file for subreddit/user names")
        print("-u --user      | Input redditor name")
        print("-s --subreddit | Input subreddit name")
        print("               | ")
        print("-c --csv       | Export results to csv")
        sys.exit(1)
    
    export = False

    for opt, arg in optns:
        if opt in ("-c", "--csv")
            #Save results as a CSV file
            export = True
        elif opt in ("-f", "/f", "--file"):
            ##Read file for inputs
            processFile(arg, export)
        elif opt in ("-u", "/u", "--user"):
            ##User: name provided
            code_user(arg, export) #Call code_user() and pass Redditor name
        elif opt in ("-s", "/s", "--subreddit"):
            ##Subreddit: name provided
            code_subreddit(arg, export) #Call code_subreddit() and pass Subreddit name
        elif opt in ("-h", "--help"):
            printHelp()
            sys.exit(0)
    return

def alternate():
    ##Menu if arguments are not given
    while True:
        choice = input("Would you like to download from: a user (u/), or a subreddit (r/)? ")
        if choice in ("u", "user", "u/"):
            #Ask user for input of target name
            redditorName = input("Reddit user: u/")
            #Query if user wants to download results as a csv
            csv = input('Do you want to export results to csv? [y/n]:')
            if answer.lower().startswith("y"):
                code_user(redditorName, True)
            elif answer.lower().startswith("n"):
                code_user(redditorName, False)
        elif choice in ("r", "subreddit", "r/"):
            #Ask user for input of target name
            subredditName = input("Reddit thread: r/")
            #Query if user wants to download results as a csv
            csv = input('Do you want to export results to csv? [y/n]:')
            if answer.lower().startswith("y"):
                code_subreddit(subredditName, True)
            elif answer.lower().startswith("n"):
                code_subreddit(subredditName, False)
        elif choice in ("h", "help"):
            printHelp()
            sys.exit(0)
        else:
            print("Selection ("+choice+") is invalid.")
            print("To select a user, try: u, u/, or user.")
            print("To select a subreddit, try: r, r/, or subreddit.")
            print("To exit, try: e, c, exit, cancel.")
            print()
    return

def processFile(filename, csv):
    #Get path to file where python app is
    basePath = os.path.dirname(os.path.realpath(__file__))

    #Check if file  exists
    if os.path.isfile(basePath + '\\' + filename):
        print("Reading from file " + filename)
        lineList = list()
        lineList = [line.rstrip('\n') for line in open(filename)]

        for line in lineList:
            #Remove whitespace
            line = re.sub(' +', '',line)
            #Remove tabbing
            line = re.sub(r'\t', '',line)
            if line.startswith("u/") == True:
                ##User: name provided
                code_user(line.split('/')[1], csv) #Call code_user() and pass Redditor name
                print()
            elif line.startswith("r/") == True:
                ##Subreddit: name provided
                code_subreddit(line.split('/')[1], csv) #Call code_subreddit() and pass Subreddit name
                print()
            elif line.startswith("#") ==True:
                #Skip line, as it is a comment
                pass
            else:
                print("Line is not in the correct format.")
                print("["+line+"]")
                print()
                print("For files, the username needs to be prefixed with 'u/' or 'r/'.")
                print("This is only for file input, not for command line inputs.")
    #If file does not exist
    else:
        print("File does not exist:")
        print("["+basePath + "\\" + filename + "]")
            
    return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        #Process with arguments
        main(sys.argv[1:])
    else:
        #Process without arguments
        alternate()