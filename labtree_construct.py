import pickle
from scholarly import scholarly
from tqdm import tqdm
import sys 

###############################################
# THESE ARE ALL THE VALUES YOU NEED TO CHANGE #
###############################################
file_to_open = "mahadevan.pickle" # this is the file you want to modify
file_to_save = "mahadevan_final.pickle" # the name you want to save. Can be the same as file_to_open
myauthor = "L Mahadevan" # the exact name of your author (google scholar format : Initial-space-lastname)
removepapers = True # True/False if you want to remove the papers where your author is not first or last
displayall = False # True/False if you want to print all the authors list and the publications with no abstract
###############################################

if len(sys.argv) != 6:
    print("labtree_construct runs using the script arguments...") 
else:
    print("labtree_construct runs from command line...") 
    file_to_open = argv[1]
    file_to_save = argv[2]
    myauthor = argv[3]
    removepapers = argv[4]
    displayall = argv[5]

# we open the file created by labtree_generate [CHANGE FILE NAME]
with open(file_to_open, 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    mydict = pickle.load(f)
 
# if the object is just publications, we add a "labels" field in it
# so that we can add labels in the future
if "labels" not in mydict:
    masterdict = {"pubs":mydict,"labels":{}}
else:
    masterdict = mydict

# we reformat the author field if it's not in the right format
for pub in masterdict["pubs"]:
    authorlist = masterdict["pubs"][pub]['bib']['author']
    if isinstance(authorlist, str): #it's supposed to be a list not a string
        authorlist = authorlist.split(" and ")
        masterdict["pubs"][pub]['bib']['author'] = authorlist

selected={}
n=0
toprint = ""
# we only keep the publications where the author is the one we want 
for pub in masterdict["pubs"]:
    authorlist = masterdict["pubs"][pub]['bib']['author']
    if " and " in authorlist and isinstance(authorlist, str):
        authorlist = authorlist.split(" and ")
        masterdict["pubs"][pub]['bib']['author'] = authorlist
    if myauthor in masterdict["pubs"][pub]['bib']['author']:
        n+=1
        selected[n] = masterdict["pubs"][pub]
toprint = toprint + "Author was present in " + str(n) + " papers out of " + str(len(masterdict["pubs"])) + ", removed the others."

# remove papers where your author is not the first or the last author
# change removepapers to True if you want to use this function
# change myauthor by the name of your author
m=n
if removepapers:
    for pub in list(selected):
        if selected[pub]['bib']['author'][0] != myauthor and selected[pub]['bib']['author'][-1] != myauthor:
            selected.pop(pub,None)
            m-=1
    toprint = toprint+"\n"+"Author was first or last in "+str(m)+" papers out of "+str(n)+", removed the others."
            
# we display the list of authors to check if it's right
if displayall:
    for pub in selected:
        print(selected[pub]['bib']['author'])
        if "abstract" not in selected[pub]['bib']:
            print(selected[pub]['bib'])


# then when we're done, we update masterdict with the new pubs
masterdict["pubs"] = selected

print(toprint)

with open(file_to_save, 'wb') as f:
    pickle.dump(masterdict, f, pickle.HIGHEST_PROTOCOL)