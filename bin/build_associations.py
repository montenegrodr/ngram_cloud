#!/usr/bin/env python3

import os
import csv
import string
import unidecode
import nltk.corpus

from nltk import ngrams

INPUT_FILE = os.getenv('INPUT_FILE')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')
VOCAB_FILE = os.getenv('VOCAB_FILE')
stopwords = nltk.corpus.stopwords.words('portuguese')

with open(VOCAB_FILE) as h:
    vocab = {
        row[1]: row[0] for row in csv.reader(h)
    }


class Bigram:
    def __init__(self, word1, word2):
        self.word1 = min(word1, word2)
        self.word2 = max(word1, word2)
        self.weight = 0

    def inc(self):
        self.weight += 1

    def __hash__(self):
        return hash((self.word1, self.word2))

    def __eq__(self, other):
        return (self.word1, self.word2) == (other.word1, other.word2)


def reduce(w):
    return w not in stopwords


def transform(w):
    return unidecode.unidecode(
        w.lower().translate(
            str.maketrans(
                '', '', string.punctuation
            )
        )
    )


def sanitize_many(words):
    return filter(
        reduce,
        map(
            transform,
            words
        )
    )


def gen_csv_reader(dim_key, dim_value, reader):
    for row in reader:
        if row[dim_key] == dim_value:
            yield row


def gen_words(dim_key, dim_value, reader):
    for row in gen_csv_reader(dim_key, dim_value, reader):
        split = row['final_answer'].split()
        sanitized = sanitize_many(split)

        for bigrams in ngrams(sanitized, 2):
            yield bigrams[0], bigrams[1], row


def gen_bigrams(dim_key, dim_value, reader):
    for word1, word2, row in gen_words(dim_key, dim_value, reader):
        yield Bigram(word1, word2), row


def get_dimension():
    dimensions = [
        ('rate', '0'),
        ('rate', '1'),
        ('rate', '2'),
        ('rate', '3'),
        ('rate', '4'),
        ('rate', '5'),
        ('rate', '6'),
        ('rate', '7'),
        ('rate', '8'),
        ('rate', '9'),
        ('rate', '10'),
        ('solved', 'nao-resolvida'),
        ('solved', 'resolvida')
    ]
    for key, value in dimensions:
        yield key, value


def main():
    with open(OUTPUT_FILE, 'w') as h:
        writer = csv.writer(h)
        for dim_key, dim_value in get_dimension():
            counter = 0
            with open(INPUT_FILE) as f:
                knowledge_base = {}
                for bigram, row in gen_bigrams(
                        dim_key, dim_value, csv.DictReader(f)
                ):
                    if bigram.__hash__() not in knowledge_base:
                        knowledge_base[bigram.__hash__()] = bigram
                    knowledge_base[bigram.__hash__()].inc()

                for bigram in knowledge_base.values():
                    try:
                        writer.writerow([
                            vocab[bigram.word1],
                            vocab[bigram.word2],
                            bigram.weight,
                            row['rate'],
                            row['solved']
                        ])
                        counter += 1
                    except Exception as exp:
                        print(f'{bigram.word1} {bigram.word2} {bigram.weight} {exp}')


if __name__ == '__main__':
    main()
