import urllib2
from film import Film
import json
import time

def getURL(p=1):
    return "http://www.imdb.com/search/title?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2251824562&pf_rd_r=1H3XQHDTBG8ECWQ1K8T3&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=moviemeter&genres=horror&explore=title_type,genres&page={}&ref_=adv_nxt".format(p)

def getEntrys(url):
    page = urllib2.urlopen(url)

    if page.getcode() == 404:
        return None

    data = page.read()
    lines = data.split("\n")
    start = 0
    open = 0
    end = 0
    for i in range(0, len(lines)):
        line = lines[i].strip()
        if end == 0:
            if start == 0:
                if "lister-list" in line:
                    start = i

            else:
                if 'class="nav"' in line:
                    end = i
                    break
    res = lines[start:end]
    films = getFilmData(res)
    #return films
    appropriate = []
    for i in range(0, len(films)):
        film = films[i]
        geners = film.getGeners()
        if ("Horror" in geners or "Thriller" in geners):
            film.doubleCheckInfo()
            if not film.isTV():
                appropriate.append(film)
    return appropriate

def getFilmData(entrys):
    res = []
    last = -1
    for i in range(0, len(entrys)):
        line = entrys[i]
        if "lister-item mode-advanced" in line: # At the start of a new film entry
            if last != -1:
                res.append(Film.parse(entrys[last:i]))
            last = i
    res.append(Film.parse(entrys[last:]))
    return res


f = {}
for i in range(1, 2):
    url = getURL(i)
    e = getEntrys(url)
    if e == None:
        break

    if i != 1:
        time.sleep(10)
    print( "Page: {}".format(i))
    for j in range(0, len(e)):
        film = e[j]
        f[film.getIMDBid()] = film.getJSON()
        #print("{} @ {} : {} : {} : {} : TV - {}".format(film.getIMDBid(), film.getName(), film.getYear(), film.getCert(), film.getGeners(), film.isTV()))
    #print("\n\n")

fi = open("films.json", "w");
fi.write(json.dumps(f));
fi.close();
