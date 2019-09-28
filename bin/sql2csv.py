#!/usr/bin/env python3

import os
import csv
import mysql.connector
from builtins import Exception, enumerate

host = os.getenv('HOST', '')
passwd = os.getenv('DB_PASSWD', '')
user = os.getenv('DB_USER', 'root')
batch_size = os.getenv('BATCH_SIZE', 1000)
database = os.getenv('DB_NAME', 'reclameaqui')
csv_output = os.getenv('OUTPUTFILE', 'data.csv')
header = ['id', 'business', 'location', 'date', 'title', 'complaint_body',
          'final_answer', 'solved', 'again', 'rate', 'url', 'created_at',
          'store_id', 'complaint_page_id']


mydb = mysql.connector.connect(
    host=host,
    user=user,
    passwd=passwd,
    database=database
)
with open(csv_output, 'w') as h:
    writer = csv.DictWriter(
        f=h, fieldnames=header)
    writer.writeheader()
    try:
        c = 0
        offset = 0
        cursor = mydb.cursor()
        while True:
            offset += c
            query = f'select {",".join(header)} ' \
                    f'from `complaint` '  \
                    f'limit {batch_size} ' \
                    f'offset {offset};'
            cursor.execute(query)
            c = 0
            for c, row in enumerate(cursor, start=1):
                writer.writerow(
                    dict(zip(header, row))
                )
            if not c:
                break
    except Exception as e:
        print(e)
        mydb.close()
