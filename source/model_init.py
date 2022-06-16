import stanza


def init_clinical_model():
	# download and initialize a mimic pipeline with an i2b2 NER model
	stanza.download('en', package='mimic', processors={'ner': 'radiology'})
	nlp = stanza.Pipeline('en', package='mimic', processors={'ner': 'radiology'})

	return nlp

	# # annotate clinical text
	# doc = nlp('The patient had a sore throat and was treated with Cepacol lozenges.')

	# # print out all entities
	# for ent in doc.entities:
	# 	print(f'{ent.text}\t{ent.type}')


def init_model():
        stanza.download('en')
        nlp = stanza.Pipeline('en')

        return nlp
