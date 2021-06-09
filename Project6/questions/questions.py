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
    # query = set(tokenize(input("Query: ")))

    queries = [set(tokenize("What are the types of supervised learning?")),
           set(tokenize("When was Python 3.0 released?")),
           set(tokenize("How do neurons connect in a neural network?"))]
    for query in queries:

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
    txtfiles = dict()
    with os.scandir(directory) as files:
        for file in files:
            if file.path.endswith(".txt"):
                with open(file.path, encoding='UTF-8') as content:
                    txtfiles[file.name] = content.read()
    return txtfiles


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    ignore_words = nltk.corpus.stopwords.words("english")
    words = nltk.word_tokenize(document)
    words = [word.lower() for word in words if word.lower() not in ignore_words
             and not all(char in list(string.punctuation) for char in word)]
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    wordset = set()
    words_idf = dict()
    for document in documents:
        wordset.update(documents[document])
    for word in wordset:
        words_idf[word] = math.log(len(documents)/sum([word in documents[document] for document in documents]))
    return words_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    query_tf_idfs = dict()
    for file in files:
        query_tf_idfs[file] = 0
        for word in query:
            query_tf_idfs[file] += idfs[word] * files[file].count(word)
    sorted_files = [file for file in sorted(query_tf_idfs, key = lambda x: query_tf_idfs[x], reverse = True)]
    return sorted_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_idf = dict()
    sentence_query_density = dict()
    for sentence in sentences:
        sentence_idf[sentence] = sum([idfs[word] for word in query
                                     if word in sentences[sentence]])
        sentence_query_density[sentence] = sum([word in query for word in sentences[sentence]])/len(sentences[sentence])
    sorted_sentences = [sentence for sentence in
                        sorted(sentences, key = lambda x: (sentence_idf[x], sentence_query_density[x]) , reverse = True)]
    return sorted_sentences[:n]


if __name__ == "__main__":
    main()
