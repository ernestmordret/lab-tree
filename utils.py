from scholarly import scholarly, ProxyGenerator
from tqdm import tqdm
import pandas as pd
import unidecode

def fix_author(s):
    last_name = unidecode.unidecode(s.split()[-1].capitalize())
    first_name = s[0].capitalize()
    return first_name+' '+last_name

def format_pub(pub):
    bib = pub['bib']
    title = bib.get('title', '')
    pub_year = bib.get('pub_year', '')
    authors = '|'.join([fix_author(i) for i in bib['author'].split(' and ')])
    journal = bib.get('journal', '')
    abstract = bib.get('abstract', '')
    url = pub.get('pub_url', '')
    num_citations = pub.get('num_citations', '')

    return {'title': title,
            "pub_year": pub_year,
            'authors': authors,
            'journal': journal,
            'abstract': abstract,
            'url': url,
            'num_citations': num_citations,
            'reviewed': False
            }

def fetch_author(name):
    #pg = ProxyGenerator()
    #success = pg.FreeProxies()
    #print(success)
    #scholarly.use_proxy(pg)

    print('First pass author started')
    search_query = scholarly.search_author(name)
    first_author_result = next(search_query)
    author = scholarly.fill(first_author_result)
    print('First pass author complete')
    author['pub_index'] = 0
    publications = author['publications']
    for pub in publications:
        print(pub['bib']['title'])
        scholarly.fill(pub)
    df = pd.DataFrame.from_records([format_pub(pub) for pub in publications if 'journal' in pub.get('bib', {})])
    return df.to_dict('records')


