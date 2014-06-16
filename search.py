def searchdocs():

  import math

  #This code will attempt to take a set of documents and search for
  #the documents that most closely match the user's search.  

  #I am going to try to use the Inverse Document Frequency measure which gives more or less importance to
  #words based on how many documents they appear in.
  #To do this, I need to keep a running count of how many articles a given word (in the search) appears in.

  #Get a search string from the user
  userstring = input('What do you want to search for?  ')
  
  #Break the string into a list of words (so that we can form a word vector)
  userstring = userstring.lower()
  parsedstring = userstring.split()
  #Collect the unique words in parsedstring in a dictionary
  masterword_dictionary = {}
  for word in parsedstring:
   masterword_dictionary[word] = 0  #Initialize counts of all words in the search string to 0. I will
                                    #increment this each time one of these words appears in an article.
 
  #Make a list of only the unique words in the search string.  This gives the list a particular order
  masterword_list = []
  for word in masterword_dictionary.keys():
    masterword_list.append(word)

  #Open the file containing the list of article filenames and read the content into listofarticles
  listofarticles = open('articlelist')
  listofarticles = listofarticles.readlines()
  numarticles = len(listofarticles)

  #I am going to build a matrix where each row is a particular article and each 
  #column is the count of a particular word.
  wordmatrix = []

  #Loop through list of article filenames, open the article file, read the content of the article
  for a in listofarticles:
    word_dictionary = {}
    words = []
    wordvec = []
    article_title = a.strip()
    currentfile = open(article_title)
    article_words = currentfile.readlines()
    #Each line in the file is an element in article_words.  
    #We need to remove \n \t . and put all the article words into a single list
    for line in article_words:
      line = line.lower()   
      for w in line.split():  #Break the string 'line' into an array of words
        w = clean_word(w)
        words.append(w)
    #Now we have collected all the words in the article for this particular article
    #Loop over all the words and see if any are in the set of search words (in masterword_dictionary). If
    #so, keep a count of those words for this article
    for w in words:
      if w in masterword_dictionary.keys():
        word_dictionary[w] = word_dictionary.get(w,0) + 1

    #In masterword_dictionary, we are keeping a running count of the number of articles that has each masterword in it
    for w in masterword_dictionary.keys():
      if w in word_dictionary.keys():
        masterword_dictionary[w] = masterword_dictionary.get(w,0) + 1

    #Now we can run through masterword_list (a list is used to preserve the order of words that is used to create the
    #wordvec and wordmatrix) and pull out the word counts from 
    #word_dictionary, which has word counts for a particular article.  We then store
    #the word count from word_dictionary into a matrix (wordmatrix)
    for word in masterword_list:
      if word in word_dictionary.keys():
        wordvec.append(word_dictionary[word])
      else:
        wordvec.append(0)
    #Compute the length of wordvec and normalize it
    #Should it still be normalized with the use of InverseDocumentFreq.  I think so
    wordvec = normalize(wordvec)
    #Append the wordvec as a new row in the matrix
    wordmatrix.append(wordvec)

  #After finishing the loop over all articles, calculate the inverse document frequency (IDF).  This
  #factor can be multiplied by each word count to weight the word's importance
  #IDF(w) = log(N/n_w)  N = total number of docs, n_w is number of docs the word appears in
  InverseDocumentFreq = {}
  for w in masterword_dictionary.keys():
    if masterword_dictionary[w] > 0:
      InverseDocumentFreq[w] = math.log(numarticles/masterword_dictionary[w])
    else:
      InverseDocumentFreq[w] = 1

  #Now we can weight our word counts
  for row in range(len(wordmatrix)):
    for col in range(len(wordmatrix[row])):
      word_col = masterword_list[col]
      wordmatrix[row][col] = wordmatrix[row][col]*InverseDocumentFreq[word_col]
    #Normalize each row
    wordmatrix[row] = normalize(wordmatrix[row])
    

  #We have a wordmatrix.  To find the most relevant search result, we can calculate
  #the "distance" between the row in wordmatrix and a vector representing the 
  #search terms
  #Should masterword_vec have only a 1 for each word even if a word appears twice in a search?
  masterword_vec = []
  for word in masterword_list:
    masterword_vec.append(masterword_dictionary[word]*InverseDocumentFreq[word])  #The value (word count) of word
  masterword_vec = normalize(masterword_vec) 

  #print('Master Vec',masterword_vec)

  distance = []
  print('Articles and their scores (low score is best):')
  for i in range(numarticles):
    #Compute distance between masterword_vec and rows in matrix
    distance.append(vector_distance(masterword_vec,wordmatrix[i][:]))
    print(listofarticles[i].strip(),'score: %5.4f' %distance[i])

  closest_article_score = min(distance)  #Score of the best matched article
  #Now list all the articles that have the best matching score (this may be more than one article)
  for index,score in enumerate(distance):
    if score == closest_article_score:
      print('\n\nSearch Result is: ',listofarticles[index])
    
  
   

   



def vector_distance(vector1,vector2):
  import math
  if len(vector1) != len(vector2):
    print('Warning, these two vectors do not have the same length.')

  d = 0
  for i in range(len(vector1)):
    d = (vector1[i] - vector2[i])**2 + d
  d = math.sqrt(d)
  return d

 
            
def normalize(vector1):
  import math
  length = 0
  for value in vector1:
    length = length + value**2
  length = math.sqrt(length)
  if length > 0:
    for i in range(len(vector1)):
      vector1[i] = vector1[i]/length
  return vector1      
   

def clean_word(word):
  word = word.strip('.')
  word = word.strip(',')
  word = word.strip('!')
  word = word.strip('?')
  return word
