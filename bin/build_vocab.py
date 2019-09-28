#!/usr/bin/env python3

import os
import csv
import string
import unidecode
import nltk.corpus

from collections import defaultdict

INPUT_FILE = os.getenv('INPUT_FILE')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')
MIN_OCCURRENCES = os.getenv('MIN_OCCURRENCES', 10)
stopwords = nltk.corpus.stopwords.words('portuguese')


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


def gen_csv_reader():
    with open(INPUT_FILE) as h:
        reader = csv.DictReader(h)
        for row in reader:
            yield row


def gen_vocab():
    for row in gen_csv_reader():
        split = row['final_answer'].split()
        for sanitized_word in sanitize_many(split):
            yield sanitized_word


def main():
    vocab = defaultdict(int)
    for c, word in enumerate(gen_vocab(), start=1):
        vocab[word] += 1
        if c % 100000 == 0:
            print(c)

    id = 1
    with open(OUTPUT_FILE, 'w') as h:
        writer = csv.writer(h)
        for word, occurrences in vocab.items():
            if occurrences >= MIN_OCCURRENCES:
                writer.writerow([id, word, occurrences])
                id += 1


if __name__ == '__main__':
    main()
