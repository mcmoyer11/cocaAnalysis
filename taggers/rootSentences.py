#!/usr/bin/python
import nltk
from nltk import word_tokenize
from nltk import pos_tag
from nltk import RegexpParser
from nltk import collocations
from nltk.stem import WordNetLemmatizer
import pprint as pprint

import funk as f

def tagList(jsonList:list, whWord:str, collocate:str, context:str):
    for obj in jsonList:
        if not obj["sentence"] or obj["sentence"] == "": # Skip conditions
            continue

        sent = obj["sentence"]

        tagged = pos_tag(word_tokenize(sent))

        clauseType = None
        modal = None
        verb = None

        modals = ['am', 'is', 'are', 'was', 'were', 'being', 'been', 'be', 'have', 'had', 'has', 'do', 'does', 'did',' can', 'could', 'may', 'might', 'shall', 'should', 'will', 'would', 'must']

        context_wh, wh_collocate = f.get_sets(tagged, context, whWord, collocate)

        obj['context_wh'] = str(context_wh)
        obj['wh_collocate'] = str(wh_collocate)

        obj['wh'] = whWord
        obj['phrase'] = context

        try:
            #tag relative clauses
            if f.x_in_set("N", context_wh, is_pos=True) or f.x_in_set("DT", context_wh, is_pos=True) or f.x_in_set("JJ", context_wh, is_pos=True):
                clauseType = "Relative Clause"
            #tag infinitive clausesroorunl
            elif f.x_in_set("to", wh_collocate, is_pos=False):
                clauseType = "Non-Finite"
                verb = f.get_pos_word_in_set(wh_collocate, 'V')
            #wh__modal__NNP__VB 
            elif f.x_in_set(modals, wh_collocate, is_pos=False):
                clauseType = "Modal"
                modal = f.get_pos_word_in_set(wh_collocate, 'M')
                verb = f.get_pos_word_in_set(wh_collocate, 'V')
            else:
                clauseType = "Finite"
                verb = f.get_pos_word_in_set(wh_collocate, 'V')

        except:
            print("BROKE HERE: ")
            print(obj["resNumber"])
            print(sent)
            print(tagged)
            print(context_wh)
            break

        obj['clauseType'] = clauseType
        obj['modal'] = modal
        obj['verb'] = verb

    return jsonList
    


