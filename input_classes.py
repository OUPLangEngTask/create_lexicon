#pydantic classes for use in create_lexicon.py

from pydantic import BaseModel
from typing import List, Optional, Dict


#INPUT CLASSES
class Token(BaseModel):
    id: str
    text: str
    lemma: str
    pos: str
    pos_finegrained: Optional[str]
    feats: Optional[str]
    start_char: str
    end_char: str

class Sentence(BaseModel):
    sentence_text: str
    tokens: List[Token]

class SentencesCorpus(BaseModel):
    sentences: List[Sentence]