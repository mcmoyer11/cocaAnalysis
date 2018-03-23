import nltk
from nltk import word_tokenize
from nltk import pos_tag
from nltk import RegexpParser
from nltk import collocations
from nltk.stem import WordNetLemmatizer
import posConstant as c
import funk as f
import relClause as rc
import isFinite as isF
import pprint

def tagList(jsonFile:list):
    wnl = WordNetLemmatizer()

    for jsonInd in jsonFile:
        sent = jsonInd["sentence"]

        #tokenize the string
        token = word_tokenize(sent)

        #lemmatize the string (get rid of all the word endngs)
        token = f.lemList(token, wnl)

        #tag the list with their parts of speach (returns a list of tuples)
        posList:list = pos_tag(token)

        #check if the list is a relative clause
        if rc.isRelClause(posList):
            jsonInd["isRelClause"] = 'True'
        else:
            jsonInd["isRelClause"] = 'False'

        #check if the list is infinite
        if isF.isInFin(posList):
            jsonInd["isInfinite"] = 'True'
            #isModal and add modal tag
            jsonInd["modal"] = isF.retModal
        else:
            jsonInd["isInfinite"] = 'False'
            jsonInd["modal"] = 'None'
    
    return jsonFile

jsonObj = [{"resNumber": 1, "year": 2017, "medium": "SPOK", "publication": "Fox: Fox News Sunday", "sentence": "  's harmful if we let it be harmful. You know, it was Aristotle who said: focus on what you can control, and you can get a lot"}, {"resNumber": 2, "year": 2017, "medium": "SPOK", "publication": "CNN: CNN Tonight", "sentence": "  Well, just before all of this happened, we know that K.T. McFarland, who was Flynn's deputy, she's a former Fox News contributor, she had"}]

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(tagList(jsonObj))