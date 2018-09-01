#!/usr/bin/env python3
"""
Copyright 2017 Neural Networks and Deep Learning lab, MIPT
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys
from nermaster.ner.network import NER
from nermaster.ner.corpus import Corpus
import json
from nermaster.ner.utils import md5_hashsum, download_untar
from glob import glob
from nermaster.ner.utils import tokenize, lemmatize
import os


# This script provides command line interface for Russian Named Entity recognition
# Just run something like command below in terminal

def install():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    # Check existence of the model by hashsum

    if md5_hashsum(sorted(glob('model/*'))) != 'fd50a27b96b24cdabdda13795a3baae7':
        # Download and extract model
        download_url = 'http://lnsigo.mipt.ru/export/models/ner/ner_model_total_rus.tar.gz'
        download_path = 'model/'
        download_untar(download_url, download_path)

    # Load network params
    with open('model/params.json') as f:
        network_params = json.load(f)

    corpus = Corpus(dicts_filepath='model/dict.txt')
    global network
    network = NER(corpus, verbouse=False, pretrained_model_filepath='model/ner_model', **network_params)


def print_predict(sentence):
    # Split sentence into tokens
    tokens = tokenize(sentence)
    print(tokens)
    # Lemmatize every token
    tokens_lemmas = lemmatize(tokens)

    tags = network.predict_for_token_batch([tokens_lemmas])[0]
    dicti = []
    for token, tag in zip(tokens, tags):
        if token.islower() and (tag != 'B-PER' or tag != 'I-PER'):
            dicti.append({'token': token, 'tag': ''})
        elif tag == 'O':
            dicti.append({'token': token, 'tag': ''})
        else:
            dicti.append({'token': token, 'tag': tag})
    return dicti


def start(text):
    text = text.split()
    for word in text:
        print_predict(word)
