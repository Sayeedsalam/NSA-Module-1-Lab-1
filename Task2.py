from nltk.stem.porter import PorterStemmer


# create PorterStemmer object
porter_stemmer = PorterStemmer()




# read input_file content as a stream
text = "El Salvador's Minister of Foreign Affairs, Alexandra Hill, has called on citizens to stop putting their lives at risk by trying to migrate illegally."

# convert text into list of words
words = text.split()

# Create outtput file

stemmed_words = []
# for every word in our list of words
for w in words:
	# write the stemmed word to the output file
	stemmed_words.append(porter_stemmer.stem(w))
        
print("Words before stemming")
print(words)

print("Words after stemming")
print(stemmed_words)