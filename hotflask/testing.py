import db
import os
import time
import random
import sqlite3
import string

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'instance', 'hotflask.sqlite')

#run some tests on the queries
print("Getting random restaurants by ID...")
total_time = 0.0
queries_run = 0
longest_time = 0.0
for x in range(1000):
    start = time.time()
    result = db.get_restaurant(str(random.randint(0, 25000)))
    end = time.time()
    if end-start > longest_time:
        longest_time = end-start
    total_time += (end-start)
    queries_run += 1

print("Total queries run: " + str(queries_run))
print("Total time: " + "{0:0.4f}".format(total_time) + " sec")
print("Average time per query: " + "{0:0.4f}".format(total_time/queries_run) + " sec")
print("Longest query time: " + "{0:0.4f}".format(longest_time) + " sec\n")

#run some random queries
print("Executing random filterings...")
total_time = 0.0
longest_time = 0.0
queries_run = 0
for x in range(1000):
    
    lower_bound = random.uniform(0.0, 4.0)
    upper_bound = random.uniform(lower_bound, 5.0)

    randint = random.randint(1, 4)
    price_range = ""
    for x in range(randint):
        price_range += "$"

    #get a random zipcode by restaurant
    rand_rest=None
    while(not rand_rest):
        rand_rest = db.get_restaurant(str(random.randint(0, 25000)))

    start = time.time()
    result = db.do_query(lower_bound, upper_bound, price_range, rand_rest[9])
    end = time.time()

    if end-start > longest_time:
        longest_time = end-start

    total_time += (end-start)
    queries_run += 1

print("Total queries run: " + str(queries_run))
print("Total time: " + "{0:0.4f}".format(total_time) + " sec")
print("Longest time: " + "{0:0.4f}".format(longest_time) + " sec")
print("Average time per query: " + "{0:0.4f}".format(total_time/queries_run) + " sec\n")


print("Adding many random users...")
total_time = 0.0
longest_time = 0.0
queries_run = 0
usernames = []
for x in range(1000):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    rand_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    usernames.append(rand_name)
    start = time.time()
    cur.execute("INSERT INTO user VALUES (?, ?)", (rand_name, "supersecurepassword"))
    conn.commit()
    end = time.time()
    if end-start > longest_time:
        longest_time = end-start
    total_time += (end-start)
    queries_run += 1
print("Total queries run: " + str(queries_run))
print("Total time: " + "{0:0.4f}".format(total_time) + " sec")
print("Average time per query: " + "{0:0.4f}".format(total_time/queries_run) + " sec")
print("Longest query time: " + "{0:0.4f}".format(longest_time) + " sec\n")


print("Deleting the random users...")
total_time = 0.0
longest_time = 0.0
queries_run = 0
for username in usernames:
    start = time.time()
    cur.execute("DELETE FROM user WHERE username like \"" + username + "\" ;")
    conn.commit()
    end = time.time()
    if end-start > longest_time:
        longest_time = end-start
    total_time += (end-start)
    queries_run += 1
print("Total queries run: " + str(queries_run))
print("Total time: " + "{0:0.4f}".format(total_time) + " sec")
print("Average time per query: " + "{0:0.4f}".format(total_time/queries_run) + " sec")
print("Longest query time: " + "{0:0.4f}".format(longest_time) + " sec\n")
