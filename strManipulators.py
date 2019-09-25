import re #Regular Expressions (RegEx)

#Function to remove Emoji & symbols from string
def simpleString(inputString):
    #Remove Emoji by encodeing in ASCII
    inputString = inputString.encode('ascii', 'ignore').decode('ascii')
    #Use RegExp to remove symbols
    inputString = re.sub(r'[^\w]', ' ', inputString)
    return inputString

#Function to remove successive whitespace
def simpleSpace(inputString):
    inputString = re.sub(' +', ' ',inputString)
    return inputString