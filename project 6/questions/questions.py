import nltk
import sys
import os
import string
import math 

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

punctuation = string.punctuation
stopwords = nltk.corpus.stopwords.words("english")

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
    files = dict()
    
    fileNames = os.listdir(directory + os.sep)
    
    # remove temp folder created by jupyter notebook
    fileNames.remove('.ipynb_checkpoints')
    
    for fileName in fileNames: 
        file = open(directory + os.sep + fileName, "r", encoding="utf8")
        files[fileName] = file.read()
        file.close() 
    
    print('--------------------> files loaded')
    print('--------------------> computing idfs in progress...')
    return files

def tokenize(document):  
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    allWords = nltk.word_tokenize(document.lower())
    
    filtered = []
    for word in allWords:
        if word not in punctuation and word not in stopwords: 
            filtered.append(word)
            
    return filtered

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = dict()
    numberOfdocuments = len(documents.keys())

    for document in documents:
        for word in documents[document]:
            appearance = checkWordAppearance(word, documents)
            words[word] = math.log(numberOfdocuments / appearance)
              
    return words

def checkWordAppearance(word, documents):
    docCounter = 0
    
    for document in documents:
        if word in documents[document]:
            docCounter += 1
            
    return docCounter
    
def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    topFiles = []
    ranking = dict()
    
    for file in files.keys():
        ranking[file] = getTfidf(query, file, files, idfs)
    
    #sort results
    ranking = {k: v for k, v in sorted(ranking.items(), key=lambda item: item[1], reverse=True)}
    
    top_files = ranking.keys()
        
    return list(top_files)[:n]

    
def getTfidf(query, file, files, idfs):
    tfidfSum = 0
    for word in query:
        if word in files[file]:
            tf = files[file].count(word)
            idf = idfs[word]
            tfidf = tf * idf
            tfidfSum += tfidf
            
    return tfidfSum
    
def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    topSentences = []
    ranking = dict()
    for s in sentences.keys():
        ranking[s] = measureSentence(query, s, sentences, idfs)

    #sort results
    ranking = {k: v for k, v in sorted(ranking.items(), key=lambda item: item[1], reverse=True)}    
        
    rankingKeys = list(ranking.keys())
    
    if n == 1:
        if ranking[rankingKeys[0]] == ranking[rankingKeys[1]]:
            topSentence = getBestSentence(ranking, ranking[rankingKeys[0]], query, sentences)
        else:
            topSentence = rankingKeys[0]
        
        topSentences.append(topSentence)
    else:
        for x in range(n - 1):
            topSentences.append(rankingKeys[x])
        if ranking[rankingKeys[n - 1]] == ranking[rankingKeys[n]]:
            topSentence = getBestSentence(ranking, ranking[rankingKeys[n]], query, sentences)
        else:
            topSentence = rankingKeys[n - 1]
        topSentences.append(topSentence)
    
    print('--------------------> best answers are: ')
    return topSentences

def getBestSentence(ranking, value, query, sentences):
    
    #filter sentences
    filteredSentences = {k: v for k, v in ranking.items() if v == value}

    processedSentences = dict()
    
    for sentence in filteredSentences.keys():
        sentenceTotalWords = len(sentences[sentence])
        wordsCounter = 0
        for word in query:
            if word in sentences[sentence]:
                wordsCounter += 1
            
        termDensity = wordsCounter / sentenceTotalWords
        processedSentences[sentence] = termDensity
        
    #sort results
    processedSentences = {k: v for k, v in sorted(processedSentences.items(), key=lambda item: item[1], reverse=True)} 
    
    return list(processedSentences.keys())[0]

def measureSentence(query, s, sentences, idfs):
    idfSum = 0
    for word in query:
        if word in sentences[s]:
            idfSum += idfs[word]
    
    return idfSum
    
    
if __name__ == "__main__":
    main()
