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
class Pipe:
    def __iter__(self):
        return self.rawIter

    def __next__(self):
        self.rawIter.next()

    def __str__(self):
        self.name

class AlephDumpReader(Pipe):
    """
    Takes in json documents, produces a dict with 'text' and 'document_id'
    """
    def __init__(self, filepath):
        def readAlephDump(path):
            with open(path, 'rU') as f:
                for line in f:
                    doc = json.loads(line)
                    for unwanted_key in set(doc.keys()) - set(['text', 'document_id']):
                        del doc[unwanted_key]
                    yield(doc)
        self.name = "AlephDump(%s)" % filepath
        self.rawIter = readAlephDump(filepath)

class Tokenizer(Pipe):
    def __init__(self, reader):
        def tokenizeDoc():
            for doc in reader:
                doc['tokens'] = word_tokenize(doc['text'])
                yield doc
        self.rawIter = tokenizeDoc()
        self.name = "nltk_word_tokenize"

class Annotator(Pipe):
    def __init__(self, reader):
        def annotateDoc(reader):
            for doc in reader:
                doc['entities'] = ne_chunk(pos_tag(doc['tokens']))
                yield doc

        self.rawIter = annotateDoc(reader)
        self.name = "nltk_ne_chunk"

class Reporter(Pipe):
    def __init__(self, reader):
        def genReporting(reader):
            for doc in reader:
                formatted = defaultdict(list)
                for ent in doc['entities']:
                    if isinstance(ent, Tree):
                        entLabel = str.join(" ", [x for x,y in ent.flatten()])
                        formatted[ent.label()].append(entLabel)
                doc['cleaned_entities'] = dict(formatted)
                yield doc

        # organize entities
        self.rawIter = genReporting(reader)
        self.name="aggregate_reporter"
