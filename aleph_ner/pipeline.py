#!/bin/env python

import json
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict

class Pipe:
    def __iter__(self):
        return self.rawIter

    def __next__(self):
        self.rawIter.next()

    def __str__(self):
        self.name

class AlephDumpReader(Pipe):
    """
    Takes in json documents, spits out the text portion as a string
    """
    def __init__(self, filepath):
        def readAlephDump(path):
            with open(path, 'rU') as f:
                for line in f:
                    doc = json.loads(line)
                    # XXX: change the pipeline to send the whole doc
                    decoded_string = doc['text']
                    yield(decoded_string)
        self.name = "AlephDump(%s)" % filepath
        self.rawIter = readAlephDump(filepath)

class Tokenizer(Pipe):
    def __init__(self, reader):
        def tokenizeDoc():
            for doc in reader:
                yield word_tokenize(doc)
        self.rawIter = tokenizeDoc()
        self.name = "nltk_word_tokenize"

class Annotator(Pipe):
    def __init__(self, reader):
        def annotateDoc(reader):
            for doc in reader:
                yield ne_chunk(pos_tag(doc))

        self.rawIter = annotateDoc(reader)
        self.name = "nltk_ne_chunk"

class Reporter(Pipe):
    def __init__(self, reader):
        def genReporting(reader):
            for doc in reader:
                formatted = defaultdict(list)
                for ent in doc:
                    if isinstance(ent, Tree):
                        entLabel = str.join(" ", [x for x,y in ent.flatten()])
                        formatted[ent.label()].append(entLabel)
                yield formatted

        # organize entities
        self.rawIter = genReporting(reader)
        self.name="aggregate_reporter"
