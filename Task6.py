# more on this can be found in http://scikit-learn.org/stable/modules/feature_extraction.html
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()

from sklearn.feature_extraction.text import TfidfTransformer
transformer = TfidfTransformer()

# define our corpus
corpus = ['Tf_idf: is a feature feature extraction tool.', 
'Word embedding: is a feature extraction extraction.',
]


# tokenize and count the word occurrences of the corpus
counts = vectorizer.fit_transform(corpus)

# print tokens produced by the CountVectorizer
print(vectorizer.get_feature_names())

tfidf = transformer.fit_transform(counts)

print("Bag-of-words Features")
print(counts.toarray())
print("\n\nTf-Idf features")
print(tfidf.toarray())

