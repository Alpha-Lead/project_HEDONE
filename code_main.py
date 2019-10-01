import sys #To handle passing in arguments
import getopt #To handle argument parsing
from code_user import code_user
from code_subreddit import code_subreddit

#getopt.getopt(args, options, [long_options])
#options="f:u:s:"

##Process arguments
def main(argv):
    try:
        options, arguments = getopt.getopt(argv, "f:u:s:h", ["file", "user", "subreddit", "help"])
    except getopt.GetoptError as err:
        print("EXCEPTION_THROWN - SECTION_arguments")
        print("Invalid arguments.")
        print("code_main.py <flag> <name/filepath>")
        print("    FLAG       |      DESCRIPTION")
        print("---------------|------------------------------------")
        print("-f --file      | Input file for subreddit/user names")
        print("-u --user      | Input redditor name")
        print("-s --subreddit | Input subreddit name")
        sys.exit(1)
    
    for opt, arg in options:
        ##Read file for inputs
        if opt in ("-f", "/f", "--file"):
            fileLocation = arg

        ##User: name provided
        elif opt in ("-u", "/u", "--user"):
            code_user(arg) #Call code_user() and pass Redditor name

        ##Subreddit: name provided
        elif opt in ("-s", "/s", "--subreddit"):
            code_subreddit(arg)

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
        elif choice in ("e", "c", "s", "exit", "cancel", "stop"):
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        #Process with arguments
        main(sys.argv[1:])
    else:
        #Process without arguments
        alternate()