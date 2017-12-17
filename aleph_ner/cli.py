import click
import pprint
from aleph_ner.pipeline import AlephDumpReader, Tokenizer, Annotator, Reporter


# TODO: Provide a subcommands: annotate, test, train, etc
@click.command()
@click.argument('path', type=click.Path(exists=True))
def annotate(path):
    """Annotate an Aleph dump with named entity recognition"""
    pipeline = Reporter(Annotator(Tokenizer(AlephDumpReader(path))))

    for doc in pipeline:
        pprint.pprint(doc)
