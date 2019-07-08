
from nltk import StanfordNERTagger
from nltk import word_tokenize





def extract_ner(text, ner_tagger):


    print("MEthod")

    current_entity = ""
    current_tag = ""

    entity_tuples = []
    ner_tags = ner_tagger.tag(word_tokenize(text))

    print(ner_tags)

    for i in range(len(ner_tags)):
        word, tag = ner_tags[i]

        if tag =='O': #means not part of an entity
            if current_tag != "":
                entity_tuples.append((current_entity.strip(), current_tag))
                current_entity = ""
                current_tag = ""

        elif current_tag != tag:
            if current_tag != "":
                entity_tuples.append((current_entity.strip(), current_tag))
            current_entity = word
            current_tag = tag
        else:
            current_entity += ' '+word
            current_tag = tag

    if current_entity != "":
        entity_tuples.append((current_entity.strip(), current_tag))

    unique_tuples = set()
    for tuple in entity_tuples:
        unique_tuples.add(tuple)

    return unique_tuples







st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz',
                           'stanford-ner.jar',
                            encoding='utf-8')

print("\n\nExtracting NERs from the document")

document = "El Salvador's Minister of Foreign Affairs, Alexandra Hill, has called on citizens to stop putting their lives at risk by trying to migrate illegally."

ner_list = extract_ner(document, st)

print(ner_list)
