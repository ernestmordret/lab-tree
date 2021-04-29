import pickle
from scholarly import scholarly
from tqdm import tqdm

# we open the file created by labtree_generate [CHANGE FILE NAME]
with open('oxman.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    mydict = pickle.load(f)
 
# if the object is just publications, we add a "labels" field in it
# so that we can add labels in the future
if "labels" not in mydict:
    masterdict = {"pubs":mydict,"labels":{}}
else:
    masterdict = mydict
 
selected={}
n=0
# we only keep the publications where the author is the one we want [CHANGE AUTHOR NAME]
for pub in masterdict["pubs"]:
    if 'N Oxman' in masterdict["pubs"][pub]['bib']['author']:
        n+=1
        selected[n] = masterdict["pubs"][pub]

# we display the list of authors to check if it's right
for pub in selected:
    print(selected[pub]['bib']['author'])   
print(n)

################### THIS SECTION RARELY WORK
################### because google scholar doesn't want
################### so it's commented

# # we fill the abstracts. This might require multiple tries so we only fill 10 at a time.
# # repeat the script as many time as necessary. 
# stop = 0
# m = 0
# for pub in tqdm(selected):
#     if selected[pub]['filled'] == True:
#         m+=1
#     if stop < 10 and selected[pub]['filled'] == False:
#         stop+=1
#         scholarly.fill(selected[pub])
#         selected[pub]['filled'] = True
#         m+=1
# print("Filling complete ! "+str(m)+"/"+str(n)+" papers filled.")

#############################

# then when we're done, we update masterdict with the new pubs
masterdict["pubs"] = selected

print(masterdict)

with open('oxman.pickle', 'wb') as f:
    pickle.dump(masterdict, f, pickle.HIGHEST_PROTOCOL)