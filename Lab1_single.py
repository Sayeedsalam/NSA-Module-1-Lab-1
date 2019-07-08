"""
This file contains all the text preprocessing steps mentioned in Lesson 1 Lab
"""


import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import os
import random
from nltk.tokenize import  word_tokenize
#Download the stopwords first
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from Task5 import extract_ner

import sys

#useful list for stopword identification
#nltk.download('stopwords')241


#Load the set of english stop words
stop_words = stopwords.words('english')
sys.stderr.flush()
file_name = input("Enter filename to process (ex: 24175_business)")

st = nltk.StanfordNERTagger('english.all.3class.distsim.crf.ser.gz',
                           'stanford-ner.jar',
                            encoding='utf-8')


folder_path = "guardian2/"

#builds acorpus with the files stored in the folder_path directory
def build_corpus(num_documents=10, folder_path="guardian2/"):

    file_names=[]
    for file_name in os.listdir(folder_path):
        file_names.append(file_name)

    if num_documents == -1:
        num_documents = len(file_names)

    random.shuffle(file_names)

    documents = []
    doc_subset = file_names[:num_documents]

    for fileName in doc_subset:
        with open(folder_path + fileName, 'r') as f:
            documents.append(f.read())

    documents_lcase = [re.sub(r'[^\w\s\d]', '', doc.lower()) for doc in documents]
    #\documents_lcase = [re.sub(r'[0-9]+', '', doc.lower()) for doc in document_lcase]
    # Replace sequences of whitespace with a space character.
    documents_lcase = [re.sub("\s+", " ", h) for h in documents_lcase]

    return documents_lcase




with open(folder_path+file_name, "r") as input_file:
    document = input_file.read()
    document_lcase = re.sub(r'[^\w\s\d]', '', document.lower()) #removing punctuation
    document_lcase = re.sub(r'[0-9]+','', document_lcase) #remove digits
    print(document_lcase)
     # Replace sequences of whitespace with a space character.
    document_lcase = re.sub("\s+", " ", document_lcase)

    print("\n\nFinding word tokenization")

    words = word_tokenize(document_lcase)

    print (words)

    print("Number of words in the document before stopwords removal:", len(words))

    print("\n\nRunning stopwords removal")

    words_filtered = []

    for w in words:
        # check if the word is a stop word
        if not w in stop_words:
            # if not write the word to the output file
            words_filtered.append(w)

    print("Number of words in the document after stopwords removal:", len(words_filtered))
    print(words_filtered)
    print("\n\nRunning stemming process")

    word_stemmed = []
    porter_stemmer = PorterStemmer()
    for w in words_filtered:
        # write the stemmed word to the output file24175_business

        word_stemmed.append(porter_stemmer.stem(w))


    print("After stemming processing")
    print(word_stemmed)


    print("\n\nGenerating Parts-Of-Speech Tags")

    sentence_tag  = nltk.pos_tag(word_tokenize(document))
    print(sentence_tag)

    print("\n\nGenrating Bag-of-Words features")
    num_articles = input("Please enter number of documents you want in the corpus, -1 to inlclude all from guardian2 folder")

    docs = build_corpus(int(num_articles))
    vectorizer = CountVectorizer(stop_words='english')

    counts = vectorizer.fit_transform(docs)
    features = vectorizer.get_feature_names()

    #print(features)

    doc_vector = vectorizer.transform([document_lcase]).toarray()

    print("Showing words with Non-Zero count")
    count = 0
    for i in range(0, len(doc_vector[0])):
        #print(doc_vector[0][i])
        if doc_vector[0][i] > 0:
            print(features[i]+": "+str(doc_vector[0][i]))
            count+= 1

    print("Length of document vector is ", len(doc_vector[0]))
    print("Number of non-zero entry from vector ", count)

    print("\n\nGenrating TF-IDF features ")
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(counts)

    result = transformer.transform(doc_vector)

    print(result)

    print("\n\nExtracting Named Entities from the document")

    ner_list = extract_ner(document, st)

    print(ner_list)






