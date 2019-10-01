#project_HEDONE
#Import dependancies
import sys #To handle passing in arguments
import getopt #To handle argument parsing

from code_user import code_user #To operate on users
from code_subreddit import code_subreddit #To operate on subreddits

##Process arguments
def main(argv):
    try:
        optns, args = getopt.getopt(argv, "f:u:s:h", ["file", "user", "subreddit", "help"])
    except getopt.GetoptError:
        print("EXCEPTION_THROWN - SECTION_arguments")
        print("Invalid arguments.")
        print("code_main.py <flag> <name/filepath>")
        print("    FLAG       |      DESCRIPTION")
        print("---------------|------------------------------------")
        print("-f --file      | Input file for subreddit/user names")
        print("-u --user      | Input redditor name")
        print("-s --subreddit | Input subreddit name")
        sys.exit(1)
    
    for opt, arg in optns:
        if opt in ("-f", "/f", "--file"):
            ##Read file for inputs
            #fileLocation = arg
            print("Yet to implement file-read feature")
        elif opt in ("-u", "/u", "--user"):
            ##User: name provided
            code_user(arg) #Call code_user() and pass Redditor name
        elif opt in ("-s", "/s", "--subreddit"):
            ##Subreddit: name provided
            code_subreddit(arg)
    return

def alternate():
    ##Menu if arguments are not given
    while True:
        choice = input("Would you like to download from: a user (u/), or a subreddit (r/)?")
        if choice in ("u", "user", "u/"):
            #Ask user for input of target name
            redditorName = input("Reddit user: u/")
            code_user(redditorName)
        elif choice in ("r", "subreddit", "r/"):
            #Ask user for input of target name
            subredditName = input("Reddit thread: r/")
            code_subreddit(subredditName)
        elif choice in ("e", "c", "exit", "cancel", "stop"):
            print("Exiting on user request...")
            sys.exit(0)
        elif choice in ("h", "help"):
            print("Python script to download all media from a reddit user or subreddit.")
            print("1) Command line use:")
            print("   >> code_main.py <flag> <input>")
            print("   Download all from list file")
            print("     - Flag: -f --file")
            print("     - Input: path to file")
            print("   Download from reddit user")
            print("     - Flag: -u --user")
            print("     - Input: Redditor username")
            print("   Download all from list file")
            print("     - Flag: -r --subreddit")
            print("     - Input: Subreddit name")
            print("2) Interactive use:")
            print("   >> code_main.py")
            sys.exit(0)
        else:
            print("Selection ("+choice+") is invalid.")
            print("To select a user, try: u, u/, or user.")
            print("To select a subreddit, try: r, r/, or subreddit.")
            print("To exit, try: e, c, exit, cancel.")
            print()
    return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        #Process with arguments
        main(sys.argv[1:])
    else:
        #Process without arguments
        alternate()