#!/bin/env python

import json
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict

# TODO: The class API is stupid, just ue functions and compose them
# TODO: Thread a document structure through the whole process
# New output format
# document
"""
    {
     "document_id": 1234,
     "entities": [["ORGANIZATION", "US. Department Of Immigration"]]
    }
"""

def AlephDumpReader(path):
    with open(path, 'rU') as f:
        for line in f:
            doc = json.loads(line)
            for unwanted_key in set(doc.keys()) - set(['text', 'document_id']):
                del doc[unwanted_key]
            yield(doc)

def Tokenizer(reader):
    for doc in reader:
        doc['tokens'] = word_tokenize(doc['text'])
        yield doc

def Annotator(reader):
    for doc in reader:
        doc['entities'] = ne_chunk(pos_tag(doc['tokens']))
        yield doc


def Reporter(reader):
    for doc in reader:
        formatted = defaultdict(list)
        for ent in doc['entities']:
            if isinstance(ent, Tree):
                entLabel = str.join(" ", [x for x,y in ent.flatten()])
                formatted[ent.label()].append(entLabel)
        doc['cleaned_entities'] = dict(formatted)
        yield doc
