import urllib2
import json
import settings

# A class to store film information in
class Film:
    def __init__(self, name, cert, year, tv, geners, id):
        self.name = name
        self.cert = cert
        self.year = year
        self.tv = tv
        self.geners = []
        self.id = id
        self.poster = ""
        for i in range(0, len(geners)):
            self.geners.append(geners[i].strip())

    def getName(self):
        return self.name

    def getCert(self):
        return self.cert

    def getYear(self):
        return self.year

    def isTV(self):
        return self.tv

    def getGeners(self):
        return self.geners

    def getIMDBid(self):
        return self.id

    def getPosterURL(self):
        return self.poster

    def getJSON(self):
        return { "Title": self.name, "Year": self.year, "Poster": self.poster}

    def doubleCheckInfo(self):
        page = urllib2.urlopen("http://www.omdbapi.com/?i={}&apikey={}".format(self.id, settings.KEY))
        page = page.read()
        data = json.loads(page)
        if str(data["Response"]) == "False":
            return

        try:
            nName = data["Title"]
            nYear = data["Year"]
            nCert = data["Rated"]
            nGenre = data["Genre"]
            nTV = str(data["Type"]).strip()

            self.name = str(nName.encode("utf-8"))
            self.year = str(nYear.encode("utf-8"))
            self.cert = str(nCert.encode("utf-8"))
            self.geners = str(nGenre).split(",")
            self.tv = ("series" in nTV)
            self.poster = str(data["Poster"])
        except Exception as e:
            print e
            print("Error: {}".format(self.id))
            print(page)
            print ""

    @staticmethod
    def parse(lines):
        name = ""
        cert = ""
        year = 0
        tv = False
        geners = []
        id = 0
        for i in range(0, len(lines)):
            line = lines[i]
            if "?ref_=adv_li_tt" in line:
                id = line[20:line.rindex("/")].strip()
                name = lines[i+1][1:-4].strip()
                continue

            if "text-muted" in line:
                data = lines[i:i+10]
                for j in range(0, len(data)):
                    d = data[j].strip()
                    if "certificate" in d:
                        cert = d[d.index(">")+1:d.rindex("<")].strip()
                        if cert == "":
                            print(d)
                    elif "genre" in d:
                        geners = data[j + 1].strip()
                        geners = geners[:geners.index("<")].strip().split(",")
                    elif "lister-item-year" in d:
                        try:
                            year = d[d.rindex("(")+1:d.rindex(")")].strip()
                        except:
                            year = -1
                break
        return Film(name, cert, year, "TV" in cert, geners, id)
