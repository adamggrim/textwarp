import spacy

from textwarp.input_output import print_wrapped

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print_wrapped("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')
