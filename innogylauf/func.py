import requests
from bs4 import BeautifulSoup
import innogylauf as igl
import os

def resultsFromUrl(url, sex, startpage=0):
    assert sex in ["M", "W", None], "expects one of W|M"
    r = requests.get(url.format(str(startpage), sex))
    soup = BeautifulSoup(r.text)
    l = list()
    while soup.find(class_="alert") is None:
        for li in soup.findAll("li", class_="list-group-item"):
            try:
                res = igl.Result(sex=sex)
                res.fromLi(li)
                l.append(res)
            except:
                pass
        startpage += 1
        r = requests.get(url.format(str(startpage), sex))
        soup = BeautifulSoup(r.text)
    return l

def scrapeAndDump(filename, startpage=0):
    """
    scrapeAndDump(filename, startpage=0)
    ------------------------------------
    Prüft ob filename schon existiert (scheitert dann), ansonsten ruft die Funktion
    die Daten ab und speichert sie.

    filename:   str, Dateiname
    startpage:  int, hoch = weniger Daten (bspw. zu Testzwecken)
    """
    assert not os.path.isfile(filename), "{0} exists already, don't\
 do anything".format(filename)
    
    resultsUrl = "http://firmenlauf-essen.r.mikatiming.de\
/2019/?page={0}&event=LG&pid=list&search%5Bsex%5D={1}"

    # Die Ergebnisse werden nach Geschlechtern getrennt gespeichert
    maleL = resultsFromUrl(resultsUrl, "M", startpage=startpage)
    femaleL = resultsFromUrl(resultsUrl,"W", startpage=startpage)
    allL = maleL + femaleL

    # Tableau-Objekt
    allT = igl.Tableau(allL)

    # CSV-Datei speichern
    allT.dumpCsv("all.csv")
    return allT
