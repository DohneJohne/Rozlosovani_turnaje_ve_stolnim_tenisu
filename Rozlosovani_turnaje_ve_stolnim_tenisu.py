import pandas as pd

df = pd.read_excel("prihlaseni_hraci.xlsx")

hraci = []

class Osoba:
    def __init__(self, jmeno, prijmeni):
        self.jmeno = jmeno
        self.prijmeni = prijmeni
    def __repr__(self):
        return f"Osoba ({self.jmeno}, {self.prijmeni})"

class Hrac(Osoba):
    def __init__(self, jmeno, prijmeni, kategorie, gender, nasazeni, id_hrace, klub):
        super().__init__(jmeno, prijmeni)
        self.kategorie = kategorie
        self.gender = gender
        self.klub = klub
        self.nasazeni = nasazeni
        self.id_hrace = id_hrace
    def __repr__(self):
        return f"Hrac ({self.jmeno}, {self.prijmeni}, {self.kategorie}, {self.id_hrace}, {self.klub})"
    

class Rozhodci (Osoba):
    def __init__(self, jmeno, prijmeni, id_rozhodciho):
        super().__init__(jmeno, prijmeni)
        self.id_rozhodciho = id_rozhodciho

for _, row in df.iterrows():
    hrac = Hrac(jmeno = row["Jméno"],
                prijmeni = row["Přijmení"],
                kategorie = row["Kategorie"],
                gender= row["Gender"],
                nasazeni = row["Nasazení"],
                id_hrace= row["ID Hráče"],
                klub = row["Klub"])
    hraci.append(hrac)
