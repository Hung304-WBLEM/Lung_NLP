import copy

def get_nodule_lung_loc(clinical_doc):
    check_dict = ['Left Upper Lung', 'Right Upper Lung',
                  'Left Middle Lung', # only for patient345, 20170531
                  'Right Middle Lung',
                  'Left Lower Lung', 'Right Lower Lung',

                  'Left Upper Lobe', 'Right Upper Lobe',
                  'Left Middle Lobe', # only for patient345, 20170531
                  'Right Middle Lobe',
                  'Left Lower Lobe', 'Right Lower Lobe',

                  'Left Lung Apex', 'Right Lung Apex', # think of another idea 

                  'Left Mid Lung'
                  ]

    check_dict = [term.lower() for term in check_dict]

    subject_check_dict = ['nodule', 'lesion', 'mass', 'opacity', 'spiculated']

    # for ent in clinical_doc.entities:
    #     if ent.type == 'ANATOMY':
    #         if lower(ent.text) in check_dict:

    ret = []
    for sentence in clinical_doc.sentences:
        ret_sentence = []

        prev_2, prev_1 = None, None
        
        for idx, org_ent in enumerate(sentence.entities):
            ent = copy.deepcopy(org_ent)
            if ent.type == 'ANATOMY':
                ent.text = ent.text.replace('\n', '')
                if ent.text.lower() in check_dict:
                    # ret_sentence.append(ent)

                    ##################################################
                    for clinical_ent in sentence.entities:
                        if clinical_ent.type == 'OBSERVATION':
                            # if ent.text == '0.5 cm':
                            #     print(clinical_ent)
                            break_flag = False
                            for term in subject_check_dict:
                                if term in clinical_ent.text:
                                    ret_sentence.append(ent)
                                    break_flag = True
                                    break

                            if break_flag:
                                break

                        if clinical_ent.type == 'OBSERVATION_MODIFIER':
                            break_flag = False
                            for term in subject_check_dict:
                                if term in clinical_ent.text:
                                    ret_sentence.append(ent)
                                    break_flag = True
                                    break

                            if break_flag:
                                break

            if ent.type == 'ANATOMY_MODIFIER' and ent.text.lower() == 'apex':
                if idx < 2:
                    continue
                combine_text = ' '.join((prev_2.text, prev_1.text, ent.text))

                if combine_text.lower() in check_dict:
                    ent.text = combine_text
                    ent.type = 'ANATOMY'
                    ent.start_char = prev_2.start_char
                    ent.end_char = ent.end_char
                    # ret_sentence.append(ent)
                    ##################################################
                    for clinical_ent in sentence.entities:
                        if clinical_ent.type == 'OBSERVATION':
                            # if ent.text == '0.5 cm':
                            #     print(clinical_ent)
                            break_flag = False
                            for term in subject_check_dict:
                                if term in clinical_ent.text:
                                    ret_sentence.append(ent)
                                    break_flag = True
                                    break

                            if break_flag:
                                break

                        if clinical_ent.type == 'OBSERVATION_MODIFIER':
                            break_flag = False
                            for term in subject_check_dict:
                                if term in clinical_ent.text:
                                    ret_sentence.append(ent)
                                    break_flag = True
                                    break

                            if break_flag:
                                break

            if idx >= 1:
                prev_2 = prev_1 
            if idx >= 0:
                prev_1 = org_ent

            

        ret.append(ret_sentence)

    return ret


def get_nodule_lung_size(doc, clinical_model):
    check_dict = ['nodule', 'lesion', 'mass', 'opacity', 'spiculated']

    ret = []
    for sentence in doc.sentences:
        ret_sentence = []
        for org_ent in sentence.entities:
            ent = copy.deepcopy(org_ent)

            if ent.type == 'QUANTITY':
                # if ent.text == '0.5 cm':
                #     print(ent)
                clinical_sentence = clinical_model(sentence.text)

                for clinical_ent in clinical_sentence.entities:
                    if clinical_ent.type == 'OBSERVATION':
                        # if ent.text == '0.5 cm':
                        #     print(clinical_ent)
                        break_flag = False
                        for term in check_dict:
                            if term in clinical_ent.text:
                                ret_sentence.append(ent)
                                break_flag = True
                                break

                        if break_flag:
                            break

                    if clinical_ent.type == 'OBSERVATION_MODIFIER':
                        break_flag = False
                        for term in check_dict:
                            if term in clinical_ent.text:
                                ret_sentence.append(ent)
                                break_flag = True
                                break

                        if break_flag:
                            break

            
        ret.append(ret_sentence)

    # Concatenate all terms that could form a 3-D coord
    processed_ret = []

    for sentence in ret:
        processed_sentence = []
        cur_idx = 0

        for idx, ent in enumerate(sentence):
            # if cur_idx == len(processed_sentence):
            if idx == 0:
                processed_sentence.append(ent)
                continue
                
            if processed_sentence[cur_idx].text.endswith('x') \
                or ent.text.startswith('x'):

                processed_sentence[cur_idx].text = \
                    ' '.join((processed_sentence[cur_idx].text, ent.text))
                processed_sentence[cur_idx].end_char = ent.end_char
            else:
                processed_sentence.append(ent)
                cur_idx += 1

        processed_ret.append(processed_sentence)


    # print('ret:', ret)
    # print('processed ret:', processed_ret)
    return processed_ret


def get_nodule_lung_spiculation(doc):
    check_dict = ['spiculated', 'spiculate', 'spiculation']

    ret = []
    
    for sentence in doc.sentences:
        ret_sentence = []

        for ent in sentence.entities:
            if ent.type == 'OBSERVATION_MODIFIER':
                for term in check_dict:
                    if term in ent.text.lower():
                        ret_sentence.append(ent)
                        break

        ret.append(ret_sentence)

    return ret


def get_nodule_lung_contour(doc):
    check_dict = ['irregular', 'lobulated', 'ovoid',
                  'microlobulated', 'circumscribed']

    ret = []

    for sentence in doc.sentences:
        ret_sentence = []

        for ent in sentence.entities:
            if ent.type == 'OBSERVATION_MODIFIER':
                for term in check_dict:
                    if term in ent.text.lower():
                        ret_sentence.append(ent)
                        break

        ret.append(ret_sentence)

    return ret


def get_nodule_lung_fissure(doc):
    ret = []

    for sentence in doc.sentences:
        ret_sentence = []

        for ent in sentence.entities:
            if ent.type == 'ANATOMY':
                if 'fissure' in ent.text.lower():
                    ret_sentence.append(ent)
                    break

        ret.append(ret_sentence)

    return ret


def get_nodule_lung_pleural(doc):
    ret = []

    for sentence in doc.sentences:
        ret_sentence = []

        for ent in sentence.entities:
            if ent.type == 'ANATOMY' or ent.type == 'ANATOMY_MODIFIER':
                if 'pleural' in ent.text.lower():

                    # Check if 'effusion' appears in the sentence
                    effusion_flag = False
                    for nested_ent in sentence.entities:
                        if 'effusion' in nested_ent.text.lower():
                            effusion_flag = True
                            break

                    if not effusion_flag:
                        ret_sentence.append(ent)
                        break

        ret.append(ret_sentence)

    return ret


def count_nodule_lung(doc, clinical_model):
    nodule_sizes = get_nodule_lung_size(doc, clinical_model)

    count = sum([len(el) for el in nodule_sizes])

    return count


