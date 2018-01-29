#!/bin/env python

import json
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict

def AlephDumpReader(paths):
    for path in paths:
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
    """
    Formats the output documents, removing unused keys and flattening the 
    otherwise nested token structure.
    """
    for doc in reader:
        entities = []
        for ent in doc['entities']:
            if isinstance(ent, Tree):
                entLabel = str.join(" ", [x for x,y in ent.flatten()])
                entities.append((ent.label(), entLabel))

        # XXX: Remove unused keys, this is pretty smelly
        for unwanted_key in set(doc.keys()) - set(['document_id']):
            del doc[unwanted_key]

        doc['entities'] = entities
        yield doc
