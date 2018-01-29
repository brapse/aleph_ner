from aleph_ner.pipeline import AlephDumpReader, Tokenizer, Annotator, Reporter
import tempfile
import pytest
from nltk.tree import Tree

sample_doc = '''{"text": "Defendant John Doe was captured by U.S Immigration Services."}'''

# XXX: why is this scoped module?
@pytest.fixture(scope='module')
def with_sample_doc(request):
    f = tempfile.NamedTemporaryFile(delete=True)
    f.write(str.encode(sample_doc))
    f.flush()
    def sample_doc_teardown():
        f.close()
    request.addfinalizer(sample_doc_teardown)
    return f.name

def test_aleph_dump_reader(with_sample_doc):
    reader = AlephDumpReader([with_sample_doc])
    lines = [i for i in reader]
    assert len(lines) == 1

def test_tokenizer(with_sample_doc):
    reader = Tokenizer(AlephDumpReader([with_sample_doc]))
    lines = [i for i in reader]
    assert len(lines) == 1
    assert lines[0]['tokens'] == ['Defendant', 'John', 'Doe', 'was', 'captured', 'by', 'U.S', 'Immigration', 'Services', '.']

def test_annotator(with_sample_doc):
    reader = Annotator(Tokenizer(AlephDumpReader([with_sample_doc])))
    lines = [i for i in reader]
    assert ('Defendant', 'NNP') in lines[0]['entities']
    assert Tree('PERSON', [('John', 'NNP'), ('Doe', 'NNP')]) in lines[0]['entities']
    assert Tree('ORGANIZATION', [('U.S', 'NNP'), ('Immigration', 'NNP'), ('Services', 'NNPS')]) in lines[0]['entities']
