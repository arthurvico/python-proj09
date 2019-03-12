import csv
import string
import pylab
from operator import itemgetter

def open_file(message):
    '''This open_file function will have a try and except statement to open a file. It will promt a message so the user knows what file to input''' 
    #Create a while loop to loop is the file is not valid
    while True:
        try:
            #Get the file name
            file_name = input(message)
            #Open the File
            file_open = open(file_name, "r")
            #Return the open file
            return file_open
        except:
            #If error, print this
            print("File is not found! Try Again!")

def read_stopwords(fp):
    ''' This file will take in a file pointer and create a set of all of the words.''' 
    #Create an empty set
    stopwords = set()
    #Create a loop for every line in the file
    for line in fp:
        #Split the lines
        line_split = line.split()
        #Create another foor loop for every word in each line
        for words in line_split:
            #Add each word and make them lower case at the same time
            stopwords.add(words.lower())
    #Return the stopwords set
    return stopwords
            
        

def validate_word(word, stopwords):
    ''' This function will return true or false if the input word is inside my set of stopwords''' 
    #Create an if statement to see if the word is all letters or if it is in the stopwords set
    if word in stopwords or word.isalpha() == False:
        #If it is in stopwords or not all letters we return False
        return False
    else:
        #If other wise we return True, meaning it is a unique word
        return True

def process_lyrics(lyrics, stopwords):
    ''' This function will be inputed a string of lyrics, it will filter every single word and create a set of unique words that are not in the stopwords file''' 
    #Split the word list by a space
    word_list = lyrics.split(' ')
    #Create an empty set
    word_set = set()
    #Create a for loop to loop over each word in the word list
    for word in word_list:
        #Make the word lower case
        word = word.lower()
        #Replace a space with nothing
        word = word.replace(" ", "")
        #strip any extra space and any punctuation at the end of the word
        word = word.strip()
        for char in string.punctuation:
            word = word.strip(char)
        #If the word passes the validate_word function as true then we add the word to the set
        if validate_word(word, stopwords) == True:
            word_set.add(word)
    #We return the set
    return word_set
        
        
def read_data(fp, stopwords):
    ''' This file will read the data of the CSV file. It will output a dictionary of the data''' 
    #Create an empty dictionary
    data_dict = {}
    #Open the CSV file and read it
    reader = csv.reader(fp)
    #Strip the header (first line)
    header = fp.readline()
    #Create a for loop to loop over each line in the file
    for line in reader:
        #Set some values equal the values of columns in our file
        singer = line[0]
        song = line[1]
        lyrics = line[2]
        #Here we process the lyrics using the process_lyrics file
        lyrics = process_lyrics(lyrics, stopwords)
        #I call the update dictionary function to create a dictionary of our file
        update_dictionary(data_dict, singer, song, lyrics)
    #return the dictionary
    return data_dict
        
            
        

def update_dictionary(data_dict, singer, song, words):
    ''' This function will create a dictionary of singer, or songs and of the words'''
    #Create an if statement to see if the singer is already in the dict. if not then add it
    if singer not in data_dict:
        data_dict[singer] = {}
    #If statement if singer already in dict, add the words in the song
    if song not in data_dict[singer]:
        data_dict[singer][song] = words
        
def calculate_average_word_count(data_dict):
    ''' This function will input the data_dict and return a dictionary of average word counts. The word count will be achieved by taking total words devided by number of songs''' 
    #Create empty dict
    avg_count = {}
    #Create loop for singer in data dict
    for singer in data_dict:
        #Set values = 0
        i = 0
        n = 0
        avg_word = 0
        #Create loop for song in data dict
        for song in data_dict[singer]:
            #Add to our singer counter
            i += 1
            #For word in data dict loop
            for word in data_dict[singer][song]:
                #Add to our song counter
                n += 1
        #Calculate the avg word count
        avg_word = n/i
        #If statement to see if singer is not in avg count
        if singer not in avg_count:
            #If not, make the singer equal to the avg words
            avg_count[singer] = avg_word
    return avg_count
            
    

def find_singers_vocab(data_dict):
    '''This function will take in the data_dict and return a dictionary with a set of all unique words used by every singer''' 
    #Create empty set
    avg_word = {}
    #For sing in data_dict loop
    for singer in data_dict:
        #For song words loop in data dict
        for song,words in data_dict[singer].items():
            #if singer not in avg word then add singer and make words equal to singer
            if singer not in avg_word:
                avg_word[singer] = words
            #If singer in avg word count then compare current words w existing words
            if singer in avg_word:
                avg_word[singer] = (avg_word[singer]|words)
    return avg_word
            
            
            
def display_singers(combined_list):
    ''' This function will display the top 10 singers with the most vocab''' 
    #sort my combined list in reverse order
    combined_list = sorted(combined_list,key=itemgetter(1,2),reverse = True)
    #Print some headers
    print("{:^80s}".format("Singers by Average Word Count (TOP - 10)"))
    print("{:<20s}{:>20s}{:>20s}{:>20s}".format("Singer","Average Word Count", "Vocabulary Size", "Number of Songs"))
    print('-' * 80)
    #If statement to only print the top 10
    if len(combined_list) >= 10:
        combined_list = combined_list[0:10]
    #For loop to print every line
    for item in combined_list:
        print("{:<20s}{:>20.2f}{:>20d}{:>20d}".format(item[0],round(item[1],2), item[2], item[3]))
    

def vocab_average_plot(num_songs, vocab_counts):
    """
    Plot vocab. size vs number of songs graph
    num_songs: number of songs belong to singers (list)
    vocab_counts: vocabulary size of singers (list)
        
    """       
    pylab.scatter(num_songs, vocab_counts)
    pylab.ylabel('Vocabulary Size')
    pylab.xlabel('Number of Songs')
    pylab.title('Vocabulary Size vs Number of Songs')
    pylab.show()

def search_songs(data_dict, words):
    ''' This function will input some words and return every song containing this word''' 
    end_list = []
    tup = ()
    for singer in data_dict:
        for song in data_dict[singer]:
            if words.issubset(data_dict[singer][song]):
                tup = (singer,song)
                end_list.append(tup)
    return sorted(end_list,key=itemgetter(0,1))
                

def main():
    ''' This function will run every function together'''
    #First message
    message = 'Enter a filename for the stopwords: '
    #open first file
    fp = open_file(message)
    #Second message
    message = 'Enter a filename for the song data: '
    #open second file
    fp1 = open_file(message)
    #Call the read stopwords function
    stopwords = read_stopwords(fp)
    #Call the read data function
    data_dict = read_data(fp1,stopwords)
    #Call the calc avg word count function
    avg_count = calculate_average_word_count(data_dict)
    #Call the find singers vocab function
    singers_vocab = find_singers_vocab(data_dict)
    #Create the empty combined list
    combined_list = []
    #Create a for loop for the items in singers vocab
    for item in singers_vocab:
        singer_name = item
        avg_word = avg_count[singer_name]
        vocab_size = len(singers_vocab[singer_name])
        numb_songs = len(data_dict[singer_name])
        combined_list.append((singer_name,avg_word,vocab_size,numb_songs))
    display_singers(combined_list)
    plot_question = input("Do you want to plot (yes/no)?")
    if plot_question.lower() == "yes":
        vocab_average_plot(numb_songs, vocab_size)
    print("Search Lyrics by Words")
    word = input("Input a set of words (space separated), press enter to exit:")
    if word == "":
        quit
    search_songs(data_dict, word)
    
    #'Do you want to plot (yes/no)?: '

#    RULES = """1-) Words should not have any digit or punctuation
#2-) Word list should not include any stop-word"""
                
    #"Search Lyrics by Words"
    #"Input a set of words (space separated), press enter to exit: "
    #'Error in words!'
    #"There are {} songs containing the given words!"
    #"{:<20s} {:<s}"

if __name__ == '__main__':
    main()           