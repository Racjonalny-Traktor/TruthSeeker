from googlesearch import search
u = []
for url in search("Osama dorzeczy", stop=2):
    if 'dorzeczy.pl' in url:
        if not url.strip('/').endswith('.pl'):
            u.append(url)
            break