

import nltk
import sys
import os 
import string
import math 




FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])

    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    
    file_idfs = compute_idfs(file_words)
   
    

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)
   
    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    
    a = {}
    for file_name in os.listdir(directory):
        complete_path = os.path.join(directory,file_name)
        with open(complete_path) as file:
            a[file_name] = file.read()
    return a 
    
   

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    # can't include any words that are in in string.punctuation 
    # cant include any words that are in nltk.corpus.stopwords.words("english")


    tokens = nltk.word_tokenize(document.lower())
    lower_case_tokens = [token for token in tokens if token not in string.punctuation and token not in nltk.corpus.stopwords.words("english")]

    return lower_case_tokens


  

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    a = {} # create a new dict, a, that is same as documents, but now only lists sets of words present in document
    for document in documents:
        word_set = set()
        for word in documents[document]:
            word_set.add(word)
        a[document] = word_set 
    
    # create a new set of all words in all documents
    total_word_set = set()
    for document in documents:
        for word in documents[document]:
            total_word_set.add(word)

    idfs = {}
    for word in total_word_set:
        how_many_docs_the_word_appears_in = 0
        for document in a:
            if word in a[document]:
                how_many_docs_the_word_appears_in += 1
        idfs[word] = math.log(len(documents)/how_many_docs_the_word_appears_in)
    
    return idfs 
    
    
   
    

    




def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # create a dictionary that maps filenames to sum of the tf_idf score
    
    scores = {}
    for file in files:
        scores[file] = 0

    for file in files:
        for query_word in query:
            if query_word in files[file]:
                frequency = 0 
                for word in files[file]:
                    if word == query_word:
                        frequency += 1 
                scores[file] += (frequency * idfs[query_word])
    
    sorted_filenames = sorted(scores, key=scores.get, reverse=True)
    return sorted_filenames[:n]
    
   

    
            


    
def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    
 
    sentence_scores = {}
    for sentence in sentences:
        frequency = 0 
        score = 0 
        for query_word in query:
            if query_word in sentences[sentence]:
                score += idfs[query_word]
                frequency += 1 
        sentence_scores[sentence] = (score,frequency/len(sentences[sentence]))
    
    
    sorted_keys = [k for k, v in sorted(sentence_scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]
    return sorted_keys[:n]
    


if __name__ == "__main__":
    main()



