import re
import urllib2 as ulib
import os
from nltk import PorterStemmer
import stemming.porter2
from wordsegment import segment
from searchWeb import searchgoogle
from collections import Counter


def k_list_repeat(query):
    k = searchgoogle(query)
    seg = segment(query)
    m = []
    new_list = []
    for n in seg:
        m.append(stemming.porter2.stem(n))
    seg = " ".join(m)
    proxy = ulib.ProxyHandler({'https': "https://10.3.100.207:8080", 'http': "http://10.3.100.207:8080"})
    opener = ulib.build_opener(proxy)
    ulib.install_opener(opener)

    for i in xrange(len(k)):
        req = ulib.Request(k[i], headers={'User-Agent': "Mozilla/5.0"})
        k[i] = segment(k[i])
        l = []
        for j in k[i]:
            l.append(stemming.porter2.stem(j))
        k[i] = " ".join(k[i])
        # print k[i]
        try:
            content = ulib.urlopen(req)
            x = re.findall("<\S*?title\S*?>(.*?)<\S*?/\S*?title\S*?>", content.read())
            t = []
            for s in x:
                t.append(stemming.porter2.stem(s))
            t = " ".join(t)
            m.append(t)

        except:
            pass
    return m
arr_contain_numbers = []
l = k_list_repeat("placesinindia")

#print l
for j in xrange(len(l)):
    if(any(char.isdigit() for char in l[j])):
        line_nonum = ''.join([i for i in l[j] if not i.isdigit()])
        arr_contain_numbers.append(line_nonum)

arr_repeat = []
for i in xrange(len(arr_contain_numbers)):
    k = arr_contain_numbers.count(arr_contain_numbers[i])
    if(k>1):arr_repeat.append(arr_contain_numbers[i])

li = Counter(arr_repeat)
for x in li:
    print x,li[x]