import stanza

nlp = stanza.Pipeline('en')

# nlp = stanza.Pipeline('zh', processors='tokenize,pos')

sentence = 'Barack Obama was born in Hawaii.'
doc = nlp(sentence)
print(sentence)

for sentence in doc.sentences:
    for word in sentence.words:
        print(word.text, word.lemma, word.pos)
        
for sentence in doc.sentences:
    print('Entities:', sentence.ents)
    print('Dependencies:', sentence.dependencies)        
