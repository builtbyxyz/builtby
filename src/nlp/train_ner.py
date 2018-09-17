#!/usr/bin/env python
# coding: utf8
"""Example of training spaCy's named entity recognizer, starting off with an
existing model or a blank model.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function

import plac
import random
import json
import datetime as dt
from pathlib import Path
import spacy
import numpy as np

from data_loader import load_org_data, load_loc_data, augment_org_data, augment_org_w_loc

# example training data
# TRAIN_DATA = [
#     ('Who is Shaka Khan?', {
#         'entities': [(7, 17, 'PERSON')]
#     }),
#     ('I like London and Berlin.', {
#         'entities': [(7, 13, 'LOC'), (18, 24, 'LOC')]
#     })
# ]

TEST_DATA = [
    'ANKROM MOISAN ARCHITECTS 1505 5TH AVE #300 SEATTLE, WA 98101 206.576.1600 CONTACT: WENDY LAMB',
    'SITE WORKSHOP 222 ETRURIA STREET, #200 SEATTLE, WA 98109 206.285.3026 CONTACT: BRIAN BISHOP',
    'VULCAN, INC. 505 5TH AVE S, #900 SEATTLE, WA 98104 206.342.2000 CONTACT: ALICIA STEDMAN',
    'ANKROM MOISAN ARCHITECTS',
    'VULCAN, INC.',
    'SITE WORKSHOP',
    'Architect: Ankrom Moisan Architects',
    'Architect: Ankrom Moisan',
    'Developer: Vulcan, Inc.',
    'Landscape Architect: Site Workshop',
    'The architect who designed this building was Ankrom Moisan.',
    'Ankrom Moisan was the architect',
    'Ankrom Moisan designed this building',
    'The architect, Ankrom Moisan, designed this building',
    'The developer who owns this building is Vulcan, Inc.',
    'Vulcan, Inc. is the developer',
    'Vulcan, Inc. owns this building',
    'The developer, Vulcan, Inc., owns this building',
    '1505 5TH AVE #300 SEATTLE, WA 98101',
    '222 ETRURIA STREET, #200 SEATTLE, WA 98109',
    '505 5TH AVE S, #900 SEATTLE, WA 98104'
]

def get_train_data(train_data_path):

    ORG_DATA = load_org_data(train_data_path, qty=50, random=True)
    LOC_DATA = load_loc_data(train_data_path, qty=50, random=True)

    ORG_WITH_LOC_DATA = []
    loc_idxs = np.random.randint(0, len(LOC_DATA), len(ORG_DATA), dtype=int)
    for idx, item in enumerate(ORG_DATA):
        aug_data = augment_org_w_loc(item[0], LOC_DATA[loc_idxs[idx]][0])
        ORG_WITH_LOC_DATA.extend(aug_data) 

    aug_ORG_DATA = []
    for item in ORG_DATA:
        aug_data = augment_org_data(item[0])
        aug_ORG_DATA.extend(aug_data)
    ORG_DATA.extend(aug_ORG_DATA)

    TRAIN_DATA = []
    TRAIN_DATA.extend(ORG_DATA)
    TRAIN_DATA.extend(LOC_DATA)
    TRAIN_DATA.extend(ORG_WITH_LOC_DATA)
  
    # save training data
    save_path = "./data"
    today = dt.datetime.today().strftime('%y%m%d%H%M%S')
    save_filename = f"{save_path}/{today}_train_data.json"

    with open(save_filename, 'w') as jsonfile:
        json.dump(TRAIN_DATA, jsonfile, indent=2)

    return TRAIN_DATA


@plac.annotations(
    train_data_path=("Path to training data", "positional"),
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(train_data_path, model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""

    TRAIN_DATA = get_train_data(train_data_path)

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
            print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

        print("Testing saved model on TEST_DATA")
        for text in TEST_DATA:
            doc = nlp2(text)
            print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
            print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == '__main__':
    plac.call(main)

    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]