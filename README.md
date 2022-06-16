# Lung-NLP

## Install environment using conda package
```
conda env create -f env.yml
conda activate clinical_nlp_test
```

## Report Data
A single example report is store at `data/sample_report.txt`

## Project Pipeline
1. Read a report file from disk
2. Feed the report into Stanza model for Named Entity Recognition (NER)
3. Use rules for postprocessing to extract clinical features (e.g.: Number of lesions, Lesion location, Lesion size,...)

## Running the rules on one example report
```
python data_postprocess.py
```
This file will read the report from `data/sample_report.txt` and pass it to the Stanza model to extract all Named Entities.
The extracted entities are then go through a set of rules for postprocessing to get the final results.

## I/O Example
* Input: data/sample_report.txt
* Output: 
```
Nodules Locations: [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [{
  "text": "left lower lobe",
  "type": "ANATOMY",
  "start_char": 763,
  "end_char": 779
}], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
Nodules Size: [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [{
  "text": "2.6 x 2.3 x 2.0-cm",
  "type": "QUANTITY",
  "start_char": 720,
  "end_char": 738
}], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
Nodules Lung Spiculation: [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
Nodules Lung Contour: [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [{
  "text": "Irregular",
  "type": "OBSERVATION_MODIFIER",
  "start_char": 710,
  "end_char": 719
}], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
Nodule Fissure: [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
Nodule Pleural: [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

```

