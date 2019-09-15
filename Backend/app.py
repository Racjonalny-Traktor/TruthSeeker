from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_cors import CORS
import datetime
from googlesearch import search

import re, string

'''
    - Właścicielem praw autorskich programu Morfeusz 2 jest Instytut Podstaw Informatyki PAN.
    - Autorami i właścicielami praw autorskich danych fleksyjnych SGJP są Zygmunt Saloni, Włodzimierz Gruszczyński, Marcin
    Woliński, Robert Wołosz i Danuta Skowrońska.
    - Właścicielem praw autorskich danych fleksyjnych Polimorf jest Instytut Podstaw Informatyki PAN.

    NINIEJSZE OPROGRAMOWANIE JEST DOSTARCZONE PRZEZ WŁAŚCICIELI PRAW AUTORSKICH
    „TAKIM, JAKIE JEST”. KAŻDA, DOROZUMIANA LUB BEZPOŚREDNIO WYRAŻONA GWARANCJA,
    NIE WYŁĄCZAJĄC DOROZUMIANEJ GWARANCJI PRZYDATNOŚCI HANDLOWEJ I PRZYDATNOŚCI DO
    OKREŚLONEGO ZASTOSOWANIA, JEST WYŁĄCZONA. W ŻADNYM WYPADKU WŁAŚCICIELE PRAW
    AUTORSKICH NIE MOGĄ BYĆ ODPOWIEDZIALNI ZA JAKIEKOLWIEK BEZPOŚREDNIE, POŚREDNIE,
    INCYDENTALNE, SPECJALNE, UBOCZNE I WTÓRNE SZKODY (NIE WYŁĄCZAJĄC OBOWIĄZKU
    DOSTARCZENIA PRODUKTU ZASTĘPCZEGO LUB SERWISU, ODPOWIEDZIALNOŚCI Z TYTUŁU UTRATY
    WALORÓW UŻYTKOWYCH, UTRATY DANYCH LUB KORZYŚCI, A TAKŻE PRZERW W PRACY
    PRZEDSIĘBIORSTWA) SPOWODOWANE W JAKIKOLWIEK SPOSÓB I NA PODSTAWIE ISTNIEJĄCEJ W
    TEORII ODPOWIEDZIALNOŚCI KONTRAKTOWEJ, CAŁKOWITEJ LUB DELIKTOWEJ (WYNIKŁEJ ZARÓWNO
    Z NIEDBALSTWA JAK INNYCH POSTACI WINY), POWSTAŁE W JAKIKOLWIEK SPOSÓB W WYNIKU
    UŻYWANIA LUB MAJĄCE ZWIĄZEK Z UŻYWANIEM OPROGRAMOWANIA, NAWET JEŚLI O MOŻLIWOŚCI
    POWSTANIA TAKICH SZKÓD OSTRZEŻONO.
'''

import morfeusz2
from collections import OrderedDict

morf = morfeusz2.Morfeusz()

stopwords = ' a, aby, ach, acz, aczkolwiek, aj, albo, ale, ależ, ani, aż, bardziej, bardzo, bo, bowiem, by, byli, bynajmniej, być, był, była, było, były, będzie, będą, cali, cała, cały, ci, cię, ciebie, co, cokolwiek, coś, czasami, czasem, czemu, czy, czyli, daleko, dla, dlaczego, dlatego, do, dobrze, dokąd, dość, dużo, dwa, dwaj, dwie, dwoje, dziś, dzisiaj, gdy, gdyby, gdyż, gdzie, gdziekolwiek, gdzieś, go, i, ich, ile, im, inna, inne, inny, innych, iż, ja, ją, jak, jakaś, jakby, jaki, jakichś, jakie, jakiś, jakiż, jakkolwiek, jako, jakoś, je, jeden, jedna, jedno, jednak, jednakże, jego, jej, jemu, jest, jestem, jeszcze, jeśli, jeżeli, już, ją, każdy, kiedy, kilka, kimś, kto, ktokolwiek, ktoś, która, które, którego, której, który, których, którym, którzy, ku, lat, lecz, lub, ma, mają, mało, mam, mi, mimo, między, mną, mnie, mogą, moi, moim, moja, moje, może, możliwe, można, mój, mu, musi, my, na, nad, nam, nami, nas, nasi, nasz, nasza, nasze, naszego, naszych, natomiast, natychmiast, nawet, nią, nic, nich, nie, niech, niego, niej, niemu, nigdy, nim, nimi, niż, no, o, obok, od, około, on, ona, one, oni, ono, oraz, oto, owszem, pan, pana, pani, po, pod, podczas, pomimo, ponad, ponieważ, powinien, powinna, powinni, powinno, poza, prawie, przecież, przed, przede, przedtem, przez, przy, roku, również, sam, sama, są, się, skąd, sobie, sobą, sposób, swoje, ta, tak, taka, taki, takie, także, tam, te, tego, tej, temu, ten, teraz, też, to, tobą, tobie, toteż, trzeba, tu, tutaj, twoi, twoim, twoja, twoje, twym, twój, ty, tych, tylko, tym, u, w, wam, wami, was, wasz, wasza, wasze, we, według, wiele, wielu, więc, więcej, wszyscy, wszystkich, wszystkie, wszystkim, wszystko, wtedy, wy, właśnie, z, za, zapewne, zawsze, ze, zł, znowu, znów, został, żaden, żadna, żadne, żadnych, że, żeby'.split(',')
stopwords = [x + ' ' for x in stopwords]
def pre_process(text):
    text=text.lower()
    text=re.sub("<!--?.*?-->","",text)
    text=re.sub("(\\d|\\W)+"," ",text)
    remove_digits = str.maketrans('', '', string.digits)
    text = text.translate(remove_digits)
    text= text.strip(' ')
    for stop in stopwords:
        text = text.replace(stop, ' ')
    return text

def make_word_list(sentence):
    return [x for x in sentence.split(' ') if x != '']

def lemmatize(words):
    l = []
    for word in words:
        analysis = morf.analyse(word)
        lemat = analysis[0][2][1]
        if ':' in lemat: lemat = lemat[:lemat.find(':')]
        l.append(lemat)
    return l

def count(list):
    dict = {}
    for l in list:
        if l in dict:
            dict[l] += 1
        else:
            dict[l] = 1
    return dict

def sort_by_appears(data):
    dict = count(data)
    data = list(OrderedDict.fromkeys(data))
    return sorted(data, key=lambda x: dict[x], reverse=True)

with open('analyser/data_sets/possibly_manipulative_title_keywords.txt', 'r') as file:
    data = file.read().split('\n')

weights = sort_by_appears(data)


def is_manipulative(sentence):
    sentence = lemmatize(make_word_list(pre_process(sentence)))
    for word in sentence:
        if word in weights[:100]: return  True
    return False

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('publication_date', type=str)
parser.add_argument('domain', type=str)

def is_too_old(datestring):
    return datestring[datestring.find("20")+2:datestring.find("20")+4] != "19"

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



def get_search_domain_list(article_domain):
    if article_domain in firstPoliticalOption:
        return secondPoliticalOption
    elif article_domain in secondPoliticalOption:
        return firstPoliticalOption
    else:
        return []

def get_opposite(title, domain):
    u = []
    x = title + ' ' + domain
    for url in search(x, stop=2):
            if domain in url:
                if not url.strip('/').endswith('.pl'):
                    u.append(url)
                    break
    return u

def get_opposite_articles(title, original_domain):
    u = []
    try:
        for url in get_search_domain_list(original_domain):
            u +=  get_opposite(title, url)
            if len(u) == 3: break
    except: pass
    return u


class RateArticle(Resource):
    def post(self):
        errors = []
        args = parser.parse_args()
        opposition = get_opposite_articles(args['title'], args['domain'])
        token = 'gf3f4v36f6v3fv6i7346f' #mock
        return {
            'is_objective': is_manipulative(args['title']),
            'is_too_old': is_too_old(args['publication_date']),
            'opposition_articles': opposition,
            'feedback_token': token
        }, 200

class ProvideFeedback(Resource):
    def get(self, token, rate):
        return 200

api.add_resource(RateArticle, '/article')
api.add_resource(ProvideFeedback, '/feedback/<token>/<rate>')

if __name__ == '__main__':
    app.run(debug=True)
