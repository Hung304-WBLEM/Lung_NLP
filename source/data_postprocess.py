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


with open('../data/sample_report.txt', 'r') as f:
    report = f.read()

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

