import stanza

# download and initialize the CRAFT pipeline
stanza.download('en', package='craft')
nlp = stanza.Pipeline('en', package='craft')
# annotate example text
doc = nlp('A single-cell transcriptomic atlas characterizes ageing tissues in the mouse.')
# print out dependency tree
doc.sentences[0].print_dependencies()

# download and initialize a mimic pipeline with an i2b2 NER model
stanza.download('en', package='mimic', processors={'ner': 'radiology'})
nlp = stanza.Pipeline('en', package='mimic', processors={'ner': 'radiology'})
# annotate clinical text
doc = nlp('The patient had a sore throat and was treated with Cepacol lozenges.')
# print out all entities
for ent in doc.entities:
    print(f'{ent.text}\t{ent.type}')
