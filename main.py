import requests
from bs4 import BeautifulSoup

class result(object):
    def __init__(self, surname=None, forename=None, place=None,
                 time=None, nr=None, org=None, gender=None):
        self.surname = surname
        self.forname = forename
        self.place = place 
        self.time = time
        self.nr = nr
        self.org = org
        self.gender= gender


    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, val):
        assert val in ["m", "w", None], "expects one of w|m"
        self._gender = val

    def fromLi(self, li):
        fullname = li.find(class_="type-fullname").text
        self.surname = fullname.split(",")[0]
        self.forename = fullname.split(",")[1].split("(")[0].strip()
        self.place = li.find(class_="type-place").text
        self.time = li.find(class_="type-time").text[4:]
        self.nr = li.findAll(class_="type-field")[0].text.split(".")[1]
        self.org = li.findAll(class_="type-field")[1].text[5:]
        

resultsUrl = "http://firmenlauf-essen.r.mikatiming.de/2019/?page={0}&event=LG&pid=list&search%5Bsex%5D={1}"

r = requests.get(resultsUrl.format("1", "W"))

soup = BeautifulSoup(r.text)

l = list()
for li in soup.findAll("li", class_="list-group-item"):
    try:
        res = result()
        res.fromLi(li)
        l.append(res)
    except:
        pass


end = requests.get(resultsUrl.format("500", "W"))
endsoup = BeautifulSoup(end.text)

def resultsFromUrl(url, startpage=0, gender="W"):
    r = requests.get(url.format(str(startpage), gender))
    soup = BeautifulSoup(r.text)
    l = list()
    while soup.find(class_="alert") is None:
        for li in soup.findAll("li", class_="list-group-item"):
            try:
                res = result()
                res.fromLi(li)
                l.append(res)
            except:
                pass
        startpage += 1
        r = requests.get(url.format(str(startpage), gender))
        soup = BeautifulSoup(r.text)
    return l
