import click
import pprint
from aleph_ner.pipeline import AlephDumpReader, Tokenizer, Annotator, Reporter

@click.command()
@click.argument('paths', type=click.Path(exists=True), nargs=-1)
def annotate(paths):
    """Annotate an Aleph dump with named entity recognition"""
    pipeline = Reporter(Annotator(Tokenizer(AlephDumpReader(paths))))

    for doc in pipeline:
        pprint.pprint(doc)
