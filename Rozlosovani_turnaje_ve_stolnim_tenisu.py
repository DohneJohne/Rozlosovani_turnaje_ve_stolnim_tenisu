import pandas as pd

class Osoba:
    def __init__(self, jmeno, prijmeni):
        self.jmeno = jmeno
        self.prijmeni = prijmeni
    def __repr__(self):
        return f"Osoba ({self.jmeno}, {self.prijmeni})"

class Hrac(Osoba):
    def __init__(self, jmeno, prijmeni, gender, nasazeni, klub):
        super().__init__(jmeno, prijmeni)
        self.gender = gender
        self.klub = klub
        self.nasazeni = nasazeni
    def __repr__(self):
        return f"Hrac ({self.jmeno}, {self.prijmeni}, {self.klub})"
    
    def nacist_hrace(soubor):
        df = pd.read_excel(soubor, header=2)
        hraci = []
        for _, row in df.iterrows():
            hrac = Hrac(jmeno = row["Jméno"],
                prijmeni = row["Přijmení"],
                gender= row["Gender"],
                klub = row["Klub"],
                nasazeni = row["Nasazení"],
                )
            hraci.append(hrac)
        return hraci

    def rozradit_gender(hraci):
        muzi = []
        zeny = []

        for hrac in hraci:
            if hrac.gender() in ["M", "Muž"]:
                muzi.append(hrac)
            elif hrac.gender() in ["F", "Ž", "Žena"]:
                zeny.append(hrac)
        return muzi, zeny
    
    def serazeni_a_prepis_nasazeni(hraci):
        serazeni_hraci = sorted(hraci, key=lambda hrac: hrac.nasazeni)
        for index, hrac in enumerate(serazeni_hraci, start = 1):
            hrac.nasazeni = index
            return serazeni_hraci
    
    def zakladni_rozlosovani(pocet_hracu, serazeni_hraci, pocet_skupin):
        jednicky =[]
        dvojky = []
        trojky = []
        ctyrky = []
        petky = []
        sestky = []
        delic = pocet_hracu//pocet_skupin

        for i in serazeni_hraci.nasazeni(1,delic+1):
            serazeni_hraci.append(jednicky)
        for i in serazeni_hraci.nasazeni(delic,(delic)*2+1):
            serazeni_hraci.append(dvojky)
        for i in serazeni_hraci(delic*2, (delic*3)+1):
            serazeni_hraci.append(trojky)
        for i in serazeni_hraci(delic*3, (delic*4)+1):
            serazeni_hraci.append(ctyrky)
        for i in serazeni_hraci(delic*4, (delic*5)+1):
            serazeni_hraci.append(petky)
        for i in serazeni_hraci(delic*5, (delic*6)+1):
            serazeni_hraci.append(sestky)
        return jednicky, dvojky, trojky, ctyrky, petky, sestky
        
class Skupina:
    def __init__(self, id_skupiny, pocet_hracu_ve_skupine):
        self.id_skupiny = id_skupiny
        self.pocet_hracu_ve_skupine = pocet_hracu_ve_skupine
        self.hraci_ve_skupine = []
    def __repr__(self):
        return f"Skupina číslo {self.id_skupiny}, {self.pocet_hracu_ve_skupine} hráčů"
    
class Turnaj:
    def __init__(self, hraci):
        self.hraci = hraci
        self.skupiny = []
        self.pocet_skupin = 0

    def vytvor_skupiny(self, pocet_hracu):
        pocet_skupin_zaklad = pocet_hracu//zakladni_velikost
        zbytek = pocet_hracu% zakladni_velikost

        if pocet_hracu < 7:
            self.pocet_skupin = 1
        
        elif pocet_hracu <= 13:
            self.pocet_skupin = 2
        
        elif pocet_hracu > 13:
            zakladni_velikost = 4
            
            if zbytek%3 ==0:
                self.pocet_skupin = pocet_skupin_zaklad + 1
            else: self.pocet_skupin = pocet_skupin_zaklad 
        
        for i in range(1, self.pocet_skupin + 1):
            nova_skupina = Skupina(id_skupiny=i)
            self.skupiny.append(nova_skupina)
        
hraci = Hrac.nacist_hrace("prihlaseni_hraci.xlsx")
muzi, zeny = Hrac.rozradit_gender(hraci)
muzi = Hrac.serazeni_a_prepis_nasazeni(muzi)
zeny = Hrac.serazeni_a_prepis_nasazeni(zeny)
pocet_hracu_muzi = len(muzi)
pocet_hracu_zeny = len(zeny)        
turnaj_muzi = Turnaj(muzi)
turnaj_zeny = Turnaj(zeny)
Turnaj.vytvor_skupiny(pocet_hracu_muzi)
Turnaj.vytvor_skupiny(pocet_hracu_zeny)
pocet_skupin_muzi = turnaj_muzi.pocet_skupin
pocet_skupin_zeny = turnaj_zeny.pocet_skupin
Hrac.zakladni_rozlosovani(pocet_hracu_muzi, muzi, pocet_skupin_muzi)
Hrac.zakladni_rozlosovani(pocet_hracu_zeny, zeny, pocet_skupin_zeny)
    

