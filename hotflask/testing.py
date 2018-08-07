import db
import os
import time
import random

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'instance', 'hotflask.sqlite')

#run some tests on the queries
print("Getting random restaurants by ID...")
total_time = 0.0
queries_run = 0
for x in range(1000):
    start = time.time()
    result = db.get_restaurant(str(random.randint(0, 25000)))
    end = time.time()
    total_time += (end-start)
    queries_run += 1

print("Total queries run: " + str(queries_run))
print("Total time: " + str(total_time) + " sec")
print("Average time per query: " + str(total_time/queries_run) + " sec\n")

#run some random queries
print("Executing random filterings...")
total_time = 0.0
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

    total_time += (end-start)
    queries_run += 1

print("Total queries run: " + str(queries_run))
print("Total time: " + str(total_time) + " sec")
print("Average time per query: " + str(total_time/queries_run) + " sec\n")
    

