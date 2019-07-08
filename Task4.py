
from nltk import pos_tag
from nltk.tokenize import word_tokenize

print("\n\nGenerating Parts-Of-Speech Tags")

document = "The Republican-controlled US Senate has approved a bill to send aid to the border with Mexico, as the image of a drowned migrant family shocked the US."

sentence_tag = pos_tag(word_tokenize(document))

print(sentence_tag)