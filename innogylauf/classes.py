import pandas as pd
from pandas import DataFrame

class Result(object):
    def __init__(self, surname=None, forename=None, place=None,
                 time=None, nr=None, org=None, sex=None):
        self.surname = surname
        self.forname = forename
        self.place = place 
        self.time = time
        self.nr = nr
        self.org = org
        self.sex = sex

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, sex):
        assert sex in ["M", "W", None], "expects one of W|M"
        self._sex = sex

    def fromLi(self, li, sex=None):
        fullname = li.find(class_="type-fullname").text
        self.surname = fullname.split(",")[0]
        self.forename = fullname.split(",")[1].split("(")[0].strip()
        self.place = li.find(class_="type-place").text
        self.time = li.find(class_="type-time").text[4:]
        self.nr = li.findAll(class_="type-field")[0].text.split(".")[1]
        self.org = li.findAll(class_="type-field")[1].text[5:]

class Tableau(object):
    def __init__(self, l=list()):
        self.l = l
        self.df = True

    def dumpCsv(self, filename):
        return self.df.to_csv(filename, sep=";")

    def fromCsv(self, filename, sep=";", header=0):
        df = pd.read_csv(filename, sep=sep, header=header,
                         usecols=["surname", "forename",
                                  "place", "time", "nr", "org",
                                  "sex"])
        for index, row in df.iterrows():
            self.l.append(Result(surname=row["surname"],
                                 forename=row["forename"],
                                 place=row["place"],
                                 time=row["time"],
                                 nr=row["nr"],
                                 org=row["org"],
                                 sex=row["sex"]))
        self._df = df
        return self

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, val):
        df = DataFrame(columns=["surname", "forename",
                                "place", "time", "nr",
                                "org", "sex"])
        try:
            for i in self.l:
                df = df.append({"forename": i.forename,
                                "surname": i.surname,
                                "place": i.place,
                                "time": i.time,
                                "nr": i.nr,
                                "org": i.org,
                                "sex": i.sex},
                ignore_index = True)
        except:
            pass
        finally:
            self._df = df
