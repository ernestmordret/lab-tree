from tqdm import tqdm
from pymed import PubMed
import pickle

# change the query with your own ! [CHANGE QUERY]
pubmed = PubMed(tool="OPLR", email="clara.lehenaff@cri-paris.org")
results = pubmed.query('"trans women" OR "trans woman" OR "trans man" OR "trans men" OR "transwoman" OR "transwomen" OR "transmen" OR "transman" OR "transgender" OR "transsexual" OR "transgenderism" OR "transsexuality" OR "transsexualism"', max_results=5)

mydict = {"pubs":{},"labels":{}}

# Here we construct an OPLR dictionary file based on the pubmed API :
# here are the fields, only fields present in both articles and books ar used. (copyrights is not used)
# BOTH : "pubmed_id" "title" "abstract" "publication_date" "authors" "copyrights" "doi"
# ARTI : "keywords" "journal" "methods" "conclusions" "results" "xml"
# BOOK : "doi" "isbn" "language" "publication_type" "sections" "publisher" "publisher_location"
for pub in tqdm(results):
    authors = []
    for a in pub.authors:
        name = a['initials']+" "+a['lastname']
        authors.append(name)
    
    date = pub.publication_date.strftime("%Y-%m-%d")
    
    bib = {'abstract':pub.abstract,
           'author':authors,
           'pub_year':date,
           'title':pub.title}
    
    mydict["pubs"][int(pub.pubmed_id)] = {'bib':bib, 'pub_url':pub.doi}

with open('transhealth.pickle', 'wb') as f:
    pickle.dump(mydict, f, pickle.HIGHEST_PROTOCOL)