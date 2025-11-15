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
    
    def zakladni_rozlosovani(pocet_hracu, serazeni_hraci):
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
        
        
    hraci = nacist_hrace("prihlaseni_hraci.xlsx")
    muzi, zeny = rozradit_gender(hraci)
    muzi = serazeni_a_prepis_nasazeni(muzi)
    zeny = serazeni_a_prepis_nasazeni(zeny)
    pocet_hracu_muzi = len(muzi)
    pocet_hracu_zeny = len(zeny)
    zakladni_rozlosovani(pocet_hracu_muzi, muzi)
    zakladni_rozlosovani(pocet_hracu_zeny, zeny)

class Skupina:
    def __init__(self, id_skupiny, pocet_hracu_ve_skupine):
        self.id_skupiny = id_skupiny
        self.pocet_hracu_ve_skupine = pocet_hracu_ve_skupine
        self.hraci_ve_skupine = []
    
    def vytvor_skupiny(pocet_hracu):
        pocet_skupin_zaklad = pocet_hracu//zakladni_velikost
        zbytek = pocet_hracu% zakladni_velikost

        if pocet_hracu < 7:
            pocet_skupin = 1
        
        elif pocet_hracu <= 13:
            pocet_skupin = 2
        
        elif pocet_hracu > 13:
            zakladni_velikost = 4
            
            if zbytek%3 ==0:
                pocet_skupin = pocet_skupin_zaklad + 1
            else: pocet_skupin = pocet_skupin_zaklad 
        
    
    vytvor_skupiny(pocet_hracu_muzi)

