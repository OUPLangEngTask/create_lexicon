#pydantic classes for use in create_lexicon.py

from pydantic import BaseModel
from typing import List, Optional, Dict
        
class Wordform(BaseModel):
    wordform: str
    freq: int = 0
    feats: Optional[str]
        
    #from feats
    numtype: Optional[str]
    case: Optional[str]
    number_psor: Optional[str]
    person_psor: Optional[str]
    number: Optional[str]
    verbform: Optional[str]
    mood: Optional[str]
    person: Optional[str]
    tense: Optional[str]
    gender: Optional[str]
    aspect: Optional[str]
    prontype: Optional[str]
    voice: Optional[str]     

class Entry(BaseModel):
    lemma: str
    pos: str
    key: str 
    pos_finegrained: Optional[str]
    freq: int = 0
    wordforms: Dict[str, Wordform]

class Lexicon(BaseModel):
    entries: Dict[str, Entry]