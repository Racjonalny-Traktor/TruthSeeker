firstPoliticalOption = ['newsweek.pl',
'wyborcza.pl',
'tvn24.pl',
'polityka.pl',
'natemat.pl',
'gazeta.pl',
'wprost.pl',
]
secondPoliticalOption = [
'dorzeczy.pl',
'niezalezna.pl',
'wsieciprawdy.pl',
'gazetapolska.pl',
]

from googlesearch import search

def get_search_domain_list(article_domain):
    if article_domain in firstPoliticalOption:
        return secondPoliticalOption
    elif article_domain in secondPoliticalOption:
        return firstPoliticalOption
    else:
        return []

def get_opposite(title, domain):
    u = []
    for url in search(title + ' ' + domain, stop=3):
            if domain in url:
                if not url.strip('/').endswith('.pl'):
                    u.append(url)
                    break
    return u
def get_opposite_articles(title, original_domain):
    u = []
    for url in get_search_domain_list(original_domain):
        u +=  get_opposite(title, url)
    return u

print(get_opposite_articles('Osama bin laden', 'wyborcza.pl'))
