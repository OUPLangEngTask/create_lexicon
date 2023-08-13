import os
import json
from typing import List, Optional, Dict
from pydantic import BaseModel
from input_classes import Token, Sentence, SentencesCorpus
from output_classes import Wordform, Entry, Lexicon

#define input/output
input_file = 'sample_parsed_sentences.json'
output_filename = 'sample_lexicon.json'

#functions will add Entry objects as values in this dict with the key string as their keys
entries_dict = {}

#function to split out the features list as a dict
def parse_feats(token: Token):
    
    if token.feats:
        feats_string = token.feats
        feats_string_lowercase = feats_string.lower()
        feats_list = feats_string_lowercase.split('|')
        
        # create dict of form {'case': 'token case, 'number': 'token number' etc.}  
        feats_dict = {}
        for i in feats_list:
            feats_dict[i.split('=')[0]] = i.split('=')[1]         

    else:
        feats_dict = {}
    
    return feats_dict


#function to add a new Entry object to the dict
def add_entry(key: str, token: Token):
    
    feat_dict = parse_feats(token)

    #create a new Entry with values from the Token
    new_entry = Entry(
        lemma=token.lemma,
        pos=token.pos,
        key=key,
        pos_finegrained=token.pos_finegrained,
        freq=1,
        wordforms={token.text: Wordform(
            wordform=token.text,
            feats=token.feats,
            freq=1,
            numtype = feat_dict.get('numtype', ''),
            case=feat_dict.get('case', ''),
            number_psor=feat_dict.get('number[psor]', ''),
            person_psor=feat_dict.get('person[psor]', ''),
            number=feat_dict.get('number', ''),
            verbform=feat_dict.get('verbform', ''),
            mood=feat_dict.get('mood', ''),
            person=feat_dict.get('person', ''),
            tense=feat_dict.get('tense', ''),
            gender=feat_dict.get('gender', ''),
            aspect=feat_dict.get('aspect', ''),
            prontype=feat_dict.get('prontype', ''),
            voice=feat_dict.get('voice', '')     
            )}
        )
    
    #add the Entry to the dict
    entries_dict[key] = new_entry


#function to update an existing Entry object in the dict with new wordforms
def update_entry(key: str, token: Token):
    
    #if the wordform is already in the wordform dict, increment the frequency
    if token.text in entries_dict[key].wordforms:
        #next line is needed because there might be homographs that should in fact be counted as different wordforms because their features are different, e.g. different case, tense but same text.
        if token.feats != entries_dict[key].wordforms[token.text].feats:
            entries_dict[key].wordforms[token.text].freq += 1
        
    # if not already in, make a new object in the wordform dict with freq 1
    else:
        
        feat_dict = parse_feats(token)
        
        new_wordform = Wordform(
            wordform=token.text,
            feats=token.feats,
            freq=1,
            numtype = feat_dict.get('numtype', ''),
            case=feat_dict.get('case', ''),
            number_psor=feat_dict.get('number[sor]', ''),
            person_psor=feat_dict.get('person[psor]', ''),
            number=feat_dict.get('number', ''),
            verbform=feat_dict.get('verbform', ''),
            mood=feat_dict.get('mood', ''),
            person=feat_dict.get('person', ''),
            tense=feat_dict.get('tense', ''),
            gender=feat_dict.get('gender', ''),
            aspect=feat_dict.get('aspect', ''),
            prontype=feat_dict.get('prontype', ''),
            voice=feat_dict.get('voice', '')  
            )
        
        #add the new Wordform to the Entry's wordform dict
        entries_dict[key].wordforms[token.text] = new_wordform


#function to convert the final object to a json file
def output_as_json(obj, output_path):
    if not output_path.endswith('.json'):
        output_path += '.json'
    
    obj_json = json.loads(obj.model_dump_json(indent=4, exclude_none=True)) #change exluce_none to False to keep empty feats for each wordform
    
    with open(output_path, 'w', encoding='utf8') as json_file:
        json.dump(obj_json, json_file, indent=4, ensure_ascii=False)



####
#Run functions

#parse input doc as SentencesCorpus object
with open(input_file, 'r', encoding='utf8') as json_file:
    json_data = json_file.read()    
sentences_corpus = SentencesCorpus.model_validate_json(json_data)

print(f'Creating lexicon from {input_file}')

#iterate over sentences, tokens; either add to dict, or update exisitng dict item
for sentence in sentences_corpus.sentences:
    for token in sentence.tokens:
        
        #exclude non lexical tokens
        if token.pos != 'NUM' and token.pos != 'PUNCT':
            
            #create unique lemma key
            lemma_key = f'{token.lemma}_{token.pos}'

            if lemma_key not in entries_dict.keys():
                add_entry(lemma_key, token)
            else:
                update_entry(lemma_key, token)


#create new Lexicon object containing output of the functions
new_lexicon = Lexicon(entries=entries_dict)

#output as json
output_as_json(new_lexicon, output_filename)
print('Output saved.')