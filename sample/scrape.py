"""
scrape.py
---------
Wenn noch nicht vorhanden, lädt das Skript die Daten von der Mika-Timing
Webseite und speichert sie als csv-Datei (s.u.).

Andernfalls lädt es eine entsprechende csv-Datei in ein Tableau-Objekt.

Tableau-Objekte sind mglw. ein idiosynkratischer Umweg und üblicherweise
will man die enthaltenen Daten lieber als pandas.DataFrame verarbeiten, dafür:

>>> Tableau().df 
Empty DataFrame
Columns: [surname, forename, place, time, nr, org, sex]
Index: []
"""

from innogylauf import Tableau, resultsFromUrl, scrapeAndDump


# Wenn die Datei schon existiert, laden:
try:
    allT = scrapeAndDump("all.csv", startpage=0)
except:
    allT = Tableau().fromCsv("all.csv")

print("Der Datensatz umfasst {0} Einträge.".format(len(allT.df)))

print("Die fünf größten Teams:\n{0}".format(allT.df["org"].value_counts().head()))

