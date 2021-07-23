from bs4 import BeautifulSoup
from ner_tagged_word import tagged_word, sentence
import srsly
import typer
import warnings
from pathlib import Path
import os
import glob

import spacy
from spacy.tokens import DocBin
from spacy.tokens import Doc

nlp = spacy.blank('vi')
db = DocBin()

dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(dir_path, 'spacy_processed', 'train.spacy')
skipped_files = []
for filepath in glob.glob(os.path.join(dir_path, 'raw_data', '*.txt')):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        words = []
        ents = []
        pos = []
        soup = BeautifulSoup(text, 'html.parser')
        title = soup.find_all('title')
        extracted_raw_sentences = soup.find_all('s')
        for raw_sentence in extracted_raw_sentences:
            splitted = raw_sentence.string.split()
            for i in range(0,len(splitted), 5):
                raw_list_word = splitted[i:i+5]
                w = tagged_word(word=raw_list_word[0],
                                pos_tag=raw_list_word[1],phrase_tag=raw_list_word[2],
                                ne_tag=raw_list_word[3],ne_nested_tag=raw_list_word[4])
                words.append(w.word.replace('_',' '))
                pos.append(w.pos)
                ents.append(w.ne)
        doc = Doc(nlp.vocab, words=words, pos=pos, ents=ents)
        db.add(doc)
        print(f'Processed file: {title[0]} at {filepath}')
    except IndexError:
        print(f'Skipping file {title[0]}, please verify contents.')
        skipped_files.append(filepath)
db.to_disk(output_path)
with open('log.txt', 'w') as f:
    for file in skipped_files:
        f.write(file)
