# Verify that these libraries are installed
from scholarly import scholarly
from tqdm import tqdm
import pickle
import time
import random

pubs = {} # this dictionary will get all the publication objects

# From here you have two choices. First one is searching by author page
# (page = True), second one is searching by author name (page = False)
# by default, you should use the author page if it exists.
page = True
author = 'L Mahadevan'

if page:
    # this is your initial query. 
    search_query = scholarly.search_author(author)
    total = scholarly.fill(next(search_query))

    num = len(total['publications'])
    for i in tqdm(range(num)):
        newpub = scholarly.fill(total['publications'][i])
        pubs[i] = newpub
        
else :
    # this is your initial query. 
    search_query = scholarly.search_pubs('author:"'+author+'"')
    num = search_query._get_total_results() # google estimation of the number of results

    # we loop through the max number of queries
    for i in tqdm(range(num)):
        # and every time we save the next pub in our dictionary
        pubs[i] = next(search_query)
        # every 10 iterations, we wait 1 to 5 seconds
        # to try to make it look like we are a real user and not a bot
        remain = (i+1)%10 
        if remain == 0:
            time.sleep(1+random.random()*4)

# We then pickle our dictionary into a file [CHANGE THE NAME OF THE FILE]
with open('mahadevan.pickle', 'wb') as f:
    pickle.dump(pubs, f, pickle.HIGHEST_PROTOCOL)