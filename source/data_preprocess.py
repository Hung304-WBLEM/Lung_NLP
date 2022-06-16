import pandas as pd
import stanza
import math
import random

from collections import defaultdict
from ClinicalReports.source.model_init import init_clinical_model, init_model
from ClinicalReports.source.rules import get_nodule_lung_loc, get_nodule_lung_size
from ClinicalReports.source.rules import get_nodule_lung_spiculation, get_nodule_lung_contour
from ClinicalReports.source.rules import get_nodule_lung_fissure, get_nodule_lung_pleural
from ClinicalReports.source.rules import count_nodule_lung
from ordered_set import OrderedSet

	
model = init_model()
clinical_model = init_clinical_model()

path = '/home/hqvo2/Projects/ClinicalReports/data/lung/AllLungCases.04.22.22.xlsx'
df = pd.read_excel(path)
save_data = dict() 
save_data = defaultdict(lambda: [], save_data)

# total_reports = 0
# nan_reports = 0
# external_reports = 0

# for index, row in df.iterrows():
#         if index != 1:
#                 continue

#         total_reports += 1
#         patient_id = row['ID']
#         study_date = row['StudyDate']
#         lesion_type = row['Type of lesion']
#         lesion_num = row['Number of lesion/nodule']
#         size = row['Size of lesion']
#         location = row['Location of lesion']
#         spiculation = row['Spiculation']
#         contour = row['Contour of lesion']
#         pleural_fiss_contact = row['Pleural/fissure contact']
#         report = row['CT Reports']


#### Hanlding 'nan' case
# try:
#         doc = model(report)
# except AssertionError:
#         nan_reports += 1
#         continue

# try:
#         clinical_doc = clinical_model(report)
# except AssertionError:
#         continue
#### Hanlding 'nan' case
###########################

# if 'was not acquired at a Methodist' in report:
#         external_reports += 1
#         continue

report = '''
Study Result

Narrative
TECHNIQUE:  Intravenous contrast-enhanced CT of the chest and abdomen 
was performed. 
  
IMPRESSION: 
  
CHEST: 

     1. Heart is normal in size.  Severe left and right coronary 
artery calcifications.  No pericardial effusion. 
     2. Ascending aorta is mildly ectatic measuring 3.6 cm.  Aorta is 
moderately atherosclerotic.  Pulmonary artery is normal in size. 
     3. No mediastinal, hilar, or axillary lymphadenopathy.   
Calcified left hilar lymph node consistent with chronic granulomatous 
disease.  Thyroid and esophagus are unremarkable. 
     4. Central airways patent.  No bronchiectasis.  There are 
changes of both emphysema and fibrosis.  No honeycombing.   
     5. Irregular 2.6 x 2.3 x 2.0-cm lesion in the posterior left 
lower lobe increased in size from March 2011 compatible with 
malignancy until proven otherwise.  Remainder of the lungs are clear.   
No pleural effusion or pneumothorax. 
ABDOMEN: 

     1. Diffuse fatty infiltration of the liver.  Irregular 6-mm 
nonobstructing calculi in the interpolar right and left kidneys.   
Remainder of the solid organs are unremarkable.  Gallbladder and 
pancreaticobiliary system are nondistended. 
     2. Fusiform atherosclerotic aneurysm of the infrarenal abdominal 
aorta has shown mild interval enlargement from September 2011 now 
measuring 4.9 x 4.4 cm, previously measuring 4.7 x 4.3 cm at the same 
location.  Aneurysm is largely thrombosed although a contrast 
opacified channel measures 2 cm in maximal dimension.  Kissing iliac 
stents remain in place.  Eccentric mural thrombus mildly narrows the 
left prox stent.  Bilateral external and internal iliac arteries are 
markedly narrowed and heavily calcified.  SMA and portal venous 
system are patent.  Trace contrast is observed in the IMA. 
     3. No dilated small or large bowel.  No inflammatory changes in 
the colon. 
     4. Adenopathy, free fluid, or fluid collection. 
OTHER: 

     1. Bones intact.  Mild degenerative changes in the spine. 
     2. Mild gynecomastia
'''

doc = model(report)
clinical_doc = clinical_model(report)

nodule_loc = get_nodule_lung_loc(clinical_doc)
nodule_size = get_nodule_lung_size(doc, clinical_model)
nodule_spiculation = get_nodule_lung_spiculation(clinical_doc)
nodule_contour = get_nodule_lung_contour(clinical_doc)
nodule_fissure = get_nodule_lung_fissure(clinical_doc)
nodule_pleural = get_nodule_lung_pleural(clinical_doc)
num_nodules = count_nodule_lung(doc, clinical_model)

print('Nodules Locations:', nodule_loc)
print('Nodules Size:', nodule_size)
print('Nodules Lung Spiculation:', nodule_spiculation)
print('Nodules Lung Contour:', nodule_contour)
print('Nodule Fissure:', nodule_fissure)
print('Nodule Pleural:', nodule_pleural)
print('Nodule Count:', num_nodules)

# save_data['ID'].append(patient_id)
# save_data['StudyDate'].append(study_date)

# save_data['Number of lesion/nodule'].append(num_nodules)

# save_data['Size of lesion'].append(', '.join([el.text for sentence in nodule_size
#                                             for el in sentence]))
# save_data['Location of lesion'].append(', '.join(OrderedSet([el.text for sentence in nodule_loc
#                                                 for el in sentence])))
# save_data['Spiculation'].append(', '.join(OrderedSet([el.text for sentence in nodule_spiculation
#                                             for el in sentence])))
# save_data['Contour of lesion'].append(', '.join(OrderedSet([el.text for sentence in nodule_contour
#                                                     for el in sentence])))
# save_data['Pleural contact'].append(', '.join(OrderedSet([el.text for sentence in nodule_pleural
#                                                     for el in sentence])))
# save_data['Fissure contact'].append(', '.join(OrderedSet([el.text for sentence in nodule_fissure
#                                                     for el in sentence])))
# save_data['CT Reports'].append(report)

# print(save_data['Location of lesion'])


# print('#Total reports:', total_reports, '|'
#       '#Nan reports:', nan_reports, '|'
#       '#External reports:', external_reports, '|')
# df = pd.DataFrame(save_data)
# df.to_csv('clinical_feats_v4.csv')
