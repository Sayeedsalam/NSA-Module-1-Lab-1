#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Module 1
Lab 1
"""

import glob, os, re

from sklearn.externals._arff import unicode
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import nltk
import numpy as np

vectorizer = CountVectorizer(stop_words='english')
porter_stemmer = PorterStemmer()



def readTextFiles(path):
    textList = list()
    files = glob.glob(path+'*')
    for fle in files:
        with open(fle) as f:
            text = f.read()
            text = text.replace('\n',' ')
            text = text.strip()
            textList.append(text)
    return textList

def POS_Tagging(sentence_list):
    sentences_tag = []
    sentences_tag2 = []
    tag = []
    for each_sentence in sentence_list:
        #each_sentence = str(each_sentence, errors='ignore')
        text = word_tokenize(each_sentence)
        sentence_tag_temp = nltk.pos_tag(text)
        
        tag = []
        for (w, t) in sentence_tag_temp:
            tag.append(w+'_'+t)
        
        sentences_tag.append(sentence_tag_temp)
        sentences_tag2.append(' '.join(tag))

    #print sentences_tag[0]
    return sentences_tag, sentences_tag2

#def extractBoW(corpus):
#    vectorizer = CountVectorizer()
#    print(vectorizer.fit_transform(corpus).todense())
#    print(vectorizer.vocabulary_)
#
#
def extractTFIDF(corpus):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit_transform(corpus)
    print(vectorizer.fit_transform(corpus).todense())



def extractNER(corpus, st):   
    person_list = []
    doc_count = 1
    for text in corpus:
        #print("Extract NER")
        loc=[]    
        #text = unicode(text, errors='ignore')
        tokenized_text = word_tokenize(text)
        tagg=st.tag(tokenized_text)
        length= len(tagg)
        k=0
        i=0
        if (length == 0):
            print('error')
            return []
        while (i<length):
            loc_part=''
            if (tagg[i][1]== 'PERSON' ):
                for j in range(i, length):
                    if (tagg[j][1]== 'PERSON'):
                        loc_part += " "+ tagg[j][0].strip().replace('.','').replace('\n', '')
                        k=j+1
                    else:
                        break
                i=k
                if (loc_part !=''):
                    loc_part = loc_part.strip().replace(' ', '_')
                    if (loc_part.replace('\n', '') not in loc):
                        loc.append(loc_part.strip().replace('\n', ''))                    
            else:
                i= i+1
        #print(loc)
        person_list.append(loc)
    return person_list




if __name__=='__main__':
    
    path = './guardian2/'

    st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz',
                           'stanford-ner.jar',
                           encoding='utf-8')
    
    sections = {
            'environment':8,
            'sport':9,
            'politics':10,
            'business':1,
            'technology':2,
            'science':3,
            'film':4,
            'books':5,
            'music':6,
            'lifeandstyle':7,
        }
    documents = list()
    sectionClass = list()
    for fileName in os.listdir(path):
        with open(path + fileName, 'r') as f:
            documents.append(f.read())
            #sectionClass.append(sections[fileName[fileName.find('_') + 1:]])
            
#    lines = readTextFiles(path)
    
    # Lowercase, then replace any non-letter, space, or digit character in the headlines.
    documents_lcase = [re.sub(r'[^\w\s\d]','',doc.lower()) for doc in documents]
    # Replace sequences of whitespace with a space character.
    documents_lcase = [re.sub("\s+", " ", h) for h in documents_lcase]
    BagOfWordFeature = vectorizer.fit_transform(documents_lcase).toarray()

    # Extracting the PoS tags for each word 
    sentence_tag, sentence_tag2 = POS_Tagging(documents)
    PoSFeature = vectorizer.fit_transform(sentence_tag2).toarray()
    print("PoSFeature grabbed")
    print(PoSFeature)
    print(sentence_tag)
    print("sentence_tag printing done")
    
    #person_list = extractNER(documents, st)

    article_name = input("Please enter a document id for viewing the Named Entities (ex. 32770_technology):")

    documents = []
    with open(path + article_name, 'r') as f:

        content = f.read()

        print(content)

        documents.append(content)

        documents_lcase = [re.sub(r'[^\w\s\d]', '', doc.lower()) for doc in documents]
        # Replace sequences of whitespace with a space character.
        documents_lcase = [re.sub("\s+", " ", h) for h in documents_lcase]

        # sentence_tag, sentence_tag2 = POS_Tagging(documents)
        sentence_tag, sentence_tag2 = POS_Tagging(documents)
        print("POS Tagging")
        print(sentence_tag)
        print("NER")
        person_list = extractNER(documents, st)

        print(person_list)




