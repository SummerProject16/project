import searchWeb
import stemming
import stemming.porter2
import urllib2 as ulib
from wordsegment import segment
import re

def checkall(postags,parsedSociallists):
	j = 0
	urlsfile = open("urls.txt","w")
	for line in parsedSociallists:
		print line,
		nounpart = []
		k = 0
		splitline = line.split()
		for x in postags[j]:
			if (x is 'M' or x is '^' or x is 'Z'):
				nounpart.append(splitline[k])
			k += 1
		while True:
			try:
				googledata = searchWeb.searchgoogle(line)
				break
			except:
				#print "Connection reset Please verify"
				continue
		urlsfile.write(line+"\n"+str(googledata)+"\n")
		count = 0
		#print "Noun "+" ".join(nounpart)
		if " ".join(nounpart) == "":
			j+=1
			print "2"
			continue
		i = 1
		for site in googledata:
			try:
				if searchWeb.searchforstring(site,nounpart):
					count += 1
			except:
				print "",
			i += 1
			if i > 10:
				break
		if count > 5:
			print "1"
		else:
			print "0"
		j += 1

def test14(parsedTag,postag):
	nounpart = []
	k = 0
	ret = []
	splitline = parsedTag.split()
	for x in postag:
		if (x is 'M' or x is '^' or x is 'Z'):
			nounpart.append(splitline[k])
		k+= 1

	if " ".join(nounpart) == "":
		ret.append(2)
	while True:
		try:
			googledata = searchWeb.searchgoogle(parsedTag)
			break
		except:
			continue
	count = 0
	i = 1
	for site in googledata:
		try:
			if searchWeb.searchforstring(site,nounpart):
				count += 1
		except:
			pass
		i += 1
		if i > 10:
			break
	if count > 5:
		ret.append(1)
	else:
		ret.append(0)
	seg = parsedTag.split()
	m = []
	for n in seg:
		m.append(stemming.porter2.stem(n))
	seg = " ".join(m)
	proxy = ulib.ProxyHandler({'https': "https://10.3.100.207:8080", 'http': "http://10.3.100.207:8080"})
	opener = ulib.build_opener(proxy)
	ulib.install_opener(opener)
	counter = 0
	total = 0
	for site in googledata:
		req = ulib.Request(site, headers={'User-Agent': "Mozilla/5.0"})
		site = segment(site)
		l = []
		for j in site:
			l.append(stemming.porter2.stem(j))
		site = " ".join(l)
		try:
			content = ulib.urlopen(req)
			x = re.findall("<\S*?title\S*?>(.*?)<\S*?/\S*?title\S*?>", content.read())
			t = []
			for s in x:
				t.append(stemming.porter2.stem(s))
			t = " ".join(t)
			if ((seg in site) or (seg in t)):
				counter = counter + 1
			total = total + 1
		except:
			pass

		if (total == 10):
			ret.append("%.4f"%(float(counter)/total))
		if (total == 20):
			ret.append("%.4f"%(float(counter)/total))

	if total < 10:
		ret.append("%.4f"%(float(counter)/10.0))
		ret.append("%.4f"%(counter/20.0))
	elif total < 20:
		ret.append("%.4f"%(float(counter)/20.0))
	return ret