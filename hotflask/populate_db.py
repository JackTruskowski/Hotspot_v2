import csv
import sqlite3
import os

MAX_COUNT = 100000

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

        if count%500 == 0:
            print(str(count) + " entries added.")
        
        try:
            c.execute("INSERT INTO restaurant VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (row[0], row[10], row[1], row[2], row[6], row[7], row[8], row[13], row[9], row[5]))
            
            conn.commit()
            count += 1
            
            c.execute("INSERT INTO city VALUES (?, ?, ?, ?)", (row[5], row[4], row[3], row[11]))
            
            conn.commit()
        except Exception as e:
            continue
        
    print("Added " + str(count) + " rows to the database.")

conn.close()

