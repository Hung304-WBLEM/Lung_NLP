import pandas as pd
import stanza
import math
import random

from collections import defaultdict
from ClinicalReports.source.model_init import init_clinical_model, init_model
from ClinicalReports.source.rules import get_nodule_lung_loc, get_nodule_lung_size
from ClinicalReports.source.rules import get_nodule_lung_spiculation, get_nodule_lung_contour
from ClinicalReports.source.rules import get_nodule_lung_fissure, get_nodule_lung_pleural
from ClinicalReports.source.rules import count_nodule_lung, convert_size_cm2mm
from ordered_set import OrderedSet

	
model = init_model()
clinical_model = init_clinical_model()

path = '/home/hqvo2/Projects/ClinicalReports/data/lung/AllLungCases.04.22.22.xlsx'
df = pd.read_excel(path)
save_data = dict() 
save_data = defaultdict(lambda: [], save_data)

total_reports = 0
nan_reports = 0
external_reports = 0

for index, row in df.iterrows():
        # if index == 50:
        #         continue

        total_reports += 1
        patient_id = row['ID']
        study_date = row['StudyDate']
        lesion_type = row['Type of lesion']
        lesion_num = row['Number of lesion/nodule']
        size = row['Size of lesion']
        location = row['Location of lesion']
        spiculation = row['Spiculation']
        contour = row['Contour of lesion']
        pleural_fiss_contact = row['Pleural/fissure contact']
        report = row['CT Reports']

        print(patient_id, study_date)

        if isinstance(report, str) and \
           'was not acquired at a Methodist' in report:
                external_reports += 1
                continue

        #### Hanlding 'nan' case
        try:
                doc = model(report)
        except AssertionError:
                nan_reports += 1
                continue

        try:
                clinical_doc = clinical_model(report)
        except AssertionError:
                continue
        #### Hanlding 'nan' case
        ###########################


        nodule_loc = get_nodule_lung_loc(clinical_doc)
        nodule_size = get_nodule_lung_size(doc, clinical_model)
        nodule_spiculation = get_nodule_lung_spiculation(clinical_doc)
        nodule_contour = get_nodule_lung_contour(clinical_doc)
        nodule_fissure = get_nodule_lung_fissure(clinical_doc)
        nodule_pleural = get_nodule_lung_pleural(clinical_doc)
        num_nodules = count_nodule_lung(doc, clinical_model)

        # print('Nodules Locations:', nodule_loc)
        # print('Nodules Size:', nodule_size)
        # print('Nodules Lung Spiculation:', nodule_spiculation)
        # print('Nodules Lung Contour:', nodule_contour)
        # print('Nodule Fissure:', nodule_fissure)
        # print('Nodule Pleural:', nodule_pleural)
        # print('Nodule Count:', num_nodules)

        save_data['ID'].append(patient_id)
        save_data['StudyDate'].append(study_date)

        save_data['Number of lesion/nodule'].append(num_nodules)

        ########## Size Information ###########
        size = ', '.join([el.text for sentence in nodule_size
                          for el in sentence])
        converted_size = convert_size_cm2mm(size)

        save_data['Size of lesion'].append(size)
        save_data['Converted Size'].append(converted_size)
        #######################################

        save_data['Location of lesion'].append(', '.join(OrderedSet([el.text for sentence in nodule_loc
                                                                     for el in sentence])))
        save_data['Spiculation'].append(', '.join(OrderedSet([el.text for sentence in nodule_spiculation
                                                              for el in sentence])))
        save_data['Contour of lesion'].append(', '.join(OrderedSet([el.text for sentence in nodule_contour
                                                                    for el in sentence])))
        save_data['Pleural contact'].append(', '.join(OrderedSet([el.text for sentence in nodule_pleural
                                                                  for el in sentence])))
        save_data['Fissure contact'].append(', '.join(OrderedSet([el.text for sentence in nodule_fissure
                                                                  for el in sentence])))
        save_data['CT Reports'].append(report)



print('#Total reports:', total_reports, '|'
      '#Nan reports:', nan_reports, '|'
      '#External reports:', external_reports, '|')
df = pd.DataFrame(save_data)
df.to_csv('clinical_feats_v6.csv')
