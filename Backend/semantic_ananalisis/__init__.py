import re, string
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

with open('../analyser/data_sets/possibly_manipulative_title_keywords.txt', 'r') as file:
    data = file.read().split('\n')

weights = sort_by_appears(data)


def is_manipulative(sentence):
    sentence = lemmatize(make_word_list(pre_process(sentence)))
    for word in sentence:
        if word in weights[:100]: return  True
    return False

print(weights)