
import nltk
from nltk.corpus import stopwords

#Download the stopwords first
nltk.download('stopwords')

#Load the set of english stop words
stop_words = stopwords.words('english')

text = "The Republican-controlled US Senate has approved a bill to send aid to the border with Mexico, as the image of a drowned migrant family shocked the US."

# convert text into list of words
words = text.split()

# Create outtput file
filtered_words = []

# for every word in our list of words
for w in words:
	# check if the word is a stop word
    if not w in stop_words:
    	# if not write the word to the output file
        filtered_words.append(w)
        
print("Original number of words: "+str(len(words)))
print("Original words (before stopwords removal)")
print(words)

print("Number of words left after stopwords removal: "+str(len(filtered_words)))
print("Words retained")
print(filtered_words)
