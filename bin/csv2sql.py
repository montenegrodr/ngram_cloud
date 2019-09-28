#!/usr/bin/env python3

import os
import csv
import mysql.connector


host = os.getenv('HOST', '')
passwd = os.getenv('DB_PASSWD', '')
user = os.getenv('DB_USER', 'root')
batch_size = os.getenv('BATCH_SIZE', 1000)
database = os.getenv('DB_NAME', 'bigrams')
vocab_input = os.getenv('VOCAB_FILE')
associations_input = os.getenv('ASSOCIATIONS_FILE')


mydb = mysql.connector.connect(
    host=host,
    user=user,
    passwd=passwd,
    database=database
)

cursor = mydb.cursor()


def insert_word(id, word, hits, commit=False):
    query = '''INSERT INTO vocab VALUES ('%s', '%s', '%s');''' % (id, word, hits)
    try:
        cursor.execute(query)
        if commit:
            mydb.commit()
    except Exception as exp:
        print(query)
        print(exp)


def insert_association(word_id1, word_id2, hits, rate, solved, commit=False):
    query = f'INSERT INTO associations ' \
            f'(word1_id, word2_id, hits, rate, solved) ' \
            f'VALUES ' \
            f'({word_id1}, {word_id2}, {hits}, {int(rate)}, {solved});'
    try:
        cursor.execute(query)
        if commit:
            mydb.commit()
    except Exception as exp:
        print(query)
        print(exp)


def main():
    print('Starting to load vocab into database')

    solved_map = {
        'resolvida': 0,
        'nao-resolvida': 1
    }

    with open(vocab_input) as f:
        for c, row in enumerate(csv.reader(f)):
            commit = c % batch_size == 0
            insert_word(row[0], row[1], row[2], commit)

    mydb.commit()

    print('Starting to load association into database')
    with open(associations_input) as f:
        for c, row in enumerate(csv.reader(f)):
            commit = c % batch_size == 0
            insert_association(
                row[0],
                row[1],
                row[2],
                int(row[3]),
                solved_map[row[4]],
                commit
            )

    mydb.commit()


if __name__ == '__main__':
    main()
