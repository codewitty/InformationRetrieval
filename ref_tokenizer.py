from collections import defaultdict
import sys
import os
import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import RegexpTokenizer




# (tokenize) Notes: 
# ===========================
# for re.findall(pattern, string) used the deliminator [a-zA-Z0-9]+ because this encompasses alpha numerical characters and numbers as valid expressions to return. 

# Note that for tokens, included all words. Later may choose to remove stopwords such as "the, and, so"

# There are error handling: tokenize specifically handles the issue of a file not existing, and graciously exits.
# The remaining functions are able to deal with the event that there was an incorrect input


# (tokenize) Runtime Analysis:
# ===========================
# Therefore runtime: O(n) total time

def Tokenize(fileString): 
    
    #imported nlkt in an attempt to filter utilize its stopwords and tokenizing function
    
    #used RegexpTokenizer function from nltk that will tokenize things based on them being (an) alphanumeric character(s)
    tokenizer = RegexpTokenizer(r'\w+')
    
    #tokenizer uses NLTK's tokenize function in order to get the tokens from the string being passed in (string being the contents of the file)
    tokenizedList = tokenizer.tokenize(str(fileString))
    
    #filtering out the english stopwords from list of tokens tokenizer.tokenize() returned. 
    tokenizedList = [token for token in tokenizedList if token not in stopwords.words("english")]
    
    #returning finalized list of tokens that do not include stopwords
    return tokenizedList
    
    """
    
    try:
        f = open(TextFilePath, 'r')
    except FileNotFoundError as fnf_error:
        print("Exception ERROR: ", fnf_error)
    else: 
        tokenizedList = []
        
        for block in iter(lambda: f.read(512), ''):
            tempList = re.findall(r'[a-zA-Z0-9]+', block) 
            # reads from the string of only lowercase chars
            
            # assuming the end of the temp list is a split off word, so I am moving it to be apart of the next block and making the changes 
            # to the file current r/w pointer, moving it bacK. Even if the last token is a "full" word it will simply be reread and revaluated 
            # with the next block. Doing this is a way to allow me to read by bytes and also ensure the integrity of the "words"
            
            if(sys.getsizeof(block) >= 512):
                split = tempList.pop()
                length = len(split)
                f.seek(f.tell() - length, os.SEEK_SET) 
                # this was used after reading the documention of file operators... 
            
            tokenizedList += tempList 
            
        f.close()
        
        return tokenizedList
        """
    
    
        
            


# (computeWordFrequencies) Runtime Analysis:
# ===========================
# Therefore runtime: O(n) total time

def computeWordFrequencies(tokenizedList):
    
    if (tokenizedList == None):
        print("Input Error in computeWordFrequencies: list is of type None")
        return
    
    # the following sets a default value for the dictionary if the key doesnt exist in the dict
    tokenCount = defaultdict(int)
    
    for token in tokenizedList:
        tokenCount[token] += 1
        
    return tokenCount



# (printFreq) Notes: NA
# ===========================
# (printFreq) Runtime Analysis:
# ===========================
# Therefore runtime: O(nlogn) total time

def printFreq(Frequencies):
    
    if (Frequencies == None):
        print("Input Error in printFreq: expected dictionary is of type None")
        return
    
    for token in sorted(Frequencies, key = lambda token: Frequencies[token], reverse = True):
        print(token, " -> ", Frequencies[token])



if __name__ == '__main__':
    
    try:
        list = tokenize(sys.argv[1])
    except IndexError as in_error:
        print("Exception ERROR: ", in_error)
    else: 
        freq = computeWordFrequencies(list)
        printFreq(freq)
    
    
    
    
    # Below is for my testing purposes, and since the documentation indicated this was to be detailed with comments and error
    # catching, I thought it worth keeping just in case I decide to test again
    '''
    path = os.getcwd()
    path += "\\hello.txt"
    list = tokenize(path)
    freq = computeWordFrequencies(list)
    printFreq(freq)
    '''
    
            
            
            
            
            
            
        
        
        
    