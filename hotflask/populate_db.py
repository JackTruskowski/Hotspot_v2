import csv
import sqlite3
import os

MAX_COUNT = 100

conn = sqlite3.connect(os.path.realpath('../instance/hotflask.sqlite'))
c = conn.cursor()

with open('../data/restaurants3.csv') as f:
    reader = csv.reader(f)
    count = 0
    
    for row in reader:
        if count == 0:
            count+=1
            continue
        
        if count >= MAX_COUNT:
            break
        try:
            c.execute("INSERT INTO restaurant VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (row[0], row[10], row[1], row[2], row[6], row[7], row[8], row[13], row[9]))
            conn.commit()
        except:
            print("failed to commit an entry to the db")
        count += 1

conn.close()

