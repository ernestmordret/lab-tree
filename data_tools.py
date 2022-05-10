from scholarly import scholarly
import tqdm
from dash import html, dcc

class Publication():
    
    def __init__(self, d):
        bib = d['bib']
        self.title = bib.get('title', None)
        self.pub_year = bib.get('pub_year', None)
        self.authors = self.parse_authors(bib.get('author', []))
        self.journal = bib.get('journal', '').capitalize()
        self.abstract = bib.get('abstract', '')
        self.url = d.get('pub_url', None)
        self.num_citations = d.get('num_citations', None)
        
    def parse_authors(self, authors_string):
        authors_list = authors_string.split(' and ') 
        return [self.capitalize_author(i) for i in authors_list]
        
    def capitalize_author(self, author_name):
        return " ".join([i.capitalize() for i in author_name.split()])
    
    def to_dict(self):
        return {'title':self.title,
                'pub_year':self.pub_year,
                'authors':self.authors,
                'journal':self.journal,
                'abstract':self.abstract,
                'url':self.url,
                'num_citations':self.num_citations
               }
    
    def __str__(self):
        return f'Pub: title = {self.title}, year = {self.pub_year}'

    def __repr__(self):
        return f'Pub: title = {self.title}, year = {self.pub_year}'

        
class Author(dcc.Store):
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def fetch_author(self, name, n_max=None):
        self.data['name'] = name
        self.data['n_max'] = n_max
        
        search_query = scholarly.search_author(name)
        first_author_result = next(search_query)
        self.author = scholarly.fill(first_author_result)
        
        self.author_name = self.author['name']
        self.affiliation = self.author['affiliation']
        self.raw_publications = self.author['publications']
        self.L = min(self.n_max, len(self.raw_publications))
        self.filled_publications = []
    
    def fetch_publications(self):
        
        print('filling publications')
        self.processed_count = 0
        
        for pub in tqdm.tqdm(self.raw_publications[:self.n_max]):
            filled_pub = Publication(scholarly.fill(pub))
            self.filled_publications.append(filled_pub)
            yield filled_pub
            
    def fetch_pub(self):
        return(next(self.fetch_publications()))
            
            
    def __str__(self):
        return f'Author: {self.author_name}'

    def __repr__(self):
        return f'Author: {self.author_name}'
            