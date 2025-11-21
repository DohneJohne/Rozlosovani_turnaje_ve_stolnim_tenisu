import pandas as pd
import random

class Osoba:
    def __init__(self, jmeno, prijmeni):
        self.jmeno = jmeno
        self.prijmeni = prijmeni
    def __repr__(self):
        return f"Osoba ({self.jmeno}, {self.prijmeni})"

class Hrac(Osoba): #Hráč dědí z Osoby, reprezentuje každého hráče turnaje
    def __init__(self, jmeno, prijmeni, gender, nasazeni, klub):
        super().__init__(jmeno, prijmeni)
        self.gender = gender
        self.klub = klub
        self.nasazeni = nasazeni
    def __repr__(self):
        return f"Hrac ({self.jmeno}, {self.prijmeni}, {self.klub})"
    
    def nacist_hrace(soubor): #Python přečte Excel a přiradí k jednotlivým proměnným vlastnosti hráčů dle Excelu
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

    def rozradit_gender(hraci): #Metoda, která rozřadí Hráče pomocí genderu
        muzi = []
        zeny = []

        for hrac in hraci: #Rozřazení probíhá podle toho, co je napsané v kolonce Gender u každého hráče
            if hrac.gender.lower() in ["m", "muž"]: #U každého genderu více možností pro univerzálnost kódu
                muzi.append(hrac)
            elif hrac.gender.lower in ["f", "ž", "žena"]:#Zároveň gender převeden na malá písmena, znovu pro zvýšení univerzálnosti
                zeny.append(hrac)
        return muzi, zeny
    
    def serazeni_a_prepis_nasazeni(hraci): #Tato metoda seřadí hráče podle nasazení a přepíše jim globální nasazení ze žebříčku do lokálního nasazení turnaje
        serazeni_hraci = sorted(hraci, key=lambda hrac: hrac.nasazeni) #seřazení hráčů
        for index, hrac in enumerate(serazeni_hraci, start = 1): #přepsání nasazení
            hrac.nasazeni = index
        return serazeni_hraci
    
    def zakladni_rozlosovani_na_podskupinky(serazeni_hraci, pocet_skupin):#Metoda, která rozdělí hráče do podskupinek dle jeho nasazení a počtu skupin
        jednicky =[]
        dvojky = []
        trojky = []
        ctyrky = []
        petky = []
        sestky = []
        delic = pocet_skupin # Proměnná, která rozděluje hráče na podskupinky a dělí tyto podskupinky (12. hráč je jednička, 13. dvojka) 
#př.: Pokud přijede 48 lidí a budu mít tedy 12 skupin, tak 12 hráčů budou jedničky, 12 dvojky atd... dle jejich nasazení
        for i in serazeni_hraci[0:delic+1]:
            jednicky.append(i)
        for i in serazeni_hraci[delic:(delic)*2+1]:
            dvojky.append(i)
        for i in serazeni_hraci[delic*2: (delic*3)+1]:
            trojky.append(i)
        for i in serazeni_hraci[delic*3: (delic*4)+1]:
            ctyrky.append(i)
        for i in serazeni_hraci[delic*4: (delic*5)+1]:
            petky.append(i)
        for i in serazeni_hraci[delic*5: (delic*6)+1]:
            sestky.append(i)
        return jednicky, dvojky, trojky, ctyrky, petky, sestky
        
class Skupina: #Třída, která reprezentuje samotnou Skupinu turnaje
    def __init__(self, id_skupiny):
        self.id_skupiny = id_skupiny #Každá skupina má svoje id(číslo)
        self.hraci = []  #a čeká na přiřazení hráčů
    def __repr__(self):
        return f"Skupina číslo {self.id_skupiny}"
    
class Turnaj: #Třída reprezentující samotný turnaj, turnaj má svoje hráče a svoje skupiny
    def __init__(self, hraci): 
        self.hraci = hraci
        self.skupiny = []
        self.pocet_skupin = 0

    def vytvor_skupiny(self, pocet_hracu): #Metoda, která vytvoří počet skupin podle zadaných vlastností

        zakladni_velikost = 4 #Základní velikost skupiny jsou 4 hráči
        if pocet_hracu < 7: #Pokud přijede na turnaj méně než 7 hráčů, vytvoří se jedna skupina
            self.pocet_skupin = 1
        
        elif pocet_hracu <= 13: #Pokud na turnaj přijede 13 a méně hráčů, vytvoří se dvě skupiny
            self.pocet_skupin = 2
        
        elif pocet_hracu > 13: #Pokud na turnaj přijede více než 13 hráčů, vytvoří se počet skupin dle vlastností
            pocet_skupin_zaklad = pocet_hracu//zakladni_velikost #(1)
            zbytek = pocet_hracu% zakladni_velikost
            if zbytek%3 ==0:
                self.pocet_skupin = pocet_skupin_zaklad + 1 #(2)
            else: self.pocet_skupin = pocet_skupin_zaklad 
        #Pokud přijede počet hráčů dělitelný čtyřma, vytvoří se skupin počet dle (1), pokud po dělení 4 zbydou 1 a 2 hráči
        #Vytvoří se stejně skupin a 1 nebo 2 budou pětičlenné, pokud zbytek bude 3, vytvoří se skupina navíc a jedna ze všech skupin bude tříčlenná dle (2)
        for i in range(1, self.pocet_skupin + 1):
            nova_skupina = Skupina(id_skupiny=i)
            self.skupiny.append(nova_skupina)
    
        return self.skupiny
    
    def rozlosovani_jednicek(self,jednicky): #Metoda sloužící pro vypsání jedniček do skupin dle nasazení
        for cislo_skupiny, hrac in enumerate(jednicky, start=1):
            for skupina in self.skupiny:
                if skupina.id_skupiny == cislo_skupiny:
                    skupina.hraci.append(hrac)
                    break
    
    def rozlosovani_skupin(self, podskupinky_ze_zakladniho_rozlosovani): #Metoda pro rozlosování zbytku hráčů turnaje
        while len(podskupinky_ze_zakladniho_rozlosovani) > 0: #Pokud v podskupince je více než 0 hráčů
            hrac = random.choice(podskupinky_ze_zakladniho_rozlosovani) #Vybere náhodného hráče z podskupinky
            #Kontrola toho, aby nebyli dva hráči ze stejného klubu v jedné skupině
            vhodne_skupiny = []
            for skupina in self.skupiny:
               stejny_klub_nalezen = False
               for hrac_ve_skupine in skupina.hraci: #Podmínka pro to, když se najde duplicita klubů
                if hrac_ve_skupine.klub == hrac.klub:
                    stejny_klub_nalezen = True
            
            if stejny_klub_nalezen == False: #Pokud vybraný hráč nemá stejný klub, přidá se daná skupina do listu vhodných skupin
                    vhodne_skupiny.append(skupina)

            if len(vhodne_skupiny)>0: #Pokud je alespoň jedna vhodná skupina pro hráče, je tento hráč do té skupiny přidán
                cilova_skupina = vhodne_skupiny[0]
                cilova_skupina.hraci.append(hrac)
            else: #Pokud není vhodná skupina, přidá se hráč do skupiny s nejmenším počtem hráčů (nutné porušení pravidla o duplicitě klubů)
                nejlepsi_skupina = min(self.skupiny, key=lambda s: len(s.hraci))
                nejlepsi_skupina.hraci.append(hrac)
        
            podskupinky_ze_zakladniho_rozlosovani.remove(hrac)

#Volání tříd a metod pro správné nalosování turnaje
hraci = Hrac.nacist_hrace("prihlaseni_hraci.xlsx")
muzi, zeny = Hrac.rozradit_gender(hraci)
muzi = Hrac.serazeni_a_prepis_nasazeni(muzi)
zeny = Hrac.serazeni_a_prepis_nasazeni(zeny)
pocet_hracu_muzi = len(muzi)
pocet_hracu_zeny = len(zeny)        
turnaj_muzi = Turnaj(muzi)
turnaj_zeny = Turnaj(zeny)
turnaj_muzi.vytvor_skupiny(pocet_hracu_muzi)
turnaj_zeny.vytvor_skupiny(pocet_hracu_zeny)
pocet_skupin_muzi = turnaj_muzi.pocet_skupin
pocet_skupin_zeny = turnaj_zeny.pocet_skupin
jednicky_muzi, dvojky_muzi, trojky_muzi, ctyrky_muzi, petky_muzi, sestky_muzi =Hrac.zakladni_rozlosovani_na_podskupinky(muzi, pocet_skupin_muzi)
jednicky_zeny, dvojky_zeny, trojky_zeny, ctyrky_zeny, petky_zeny, sestky_zeny =Hrac.zakladni_rozlosovani_na_podskupinky(zeny, pocet_skupin_zeny)
turnaj_muzi.rozlosovani_jednicek(jednicky_muzi)
turnaj_zeny.rozlosovani_jednicek(jednicky_zeny)
turnaj_muzi.rozlosovani_skupin(dvojky_muzi)
turnaj_muzi.rozlosovani_skupin(trojky_muzi)
turnaj_muzi.rozlosovani_skupin(ctyrky_muzi)
turnaj_muzi.rozlosovani_skupin(petky_muzi)
turnaj_muzi.rozlosovani_skupin(sestky_muzi)
turnaj_zeny.rozlosovani_skupin(dvojky_zeny)
turnaj_zeny.rozlosovani_skupin(trojky_zeny)
turnaj_zeny.rozlosovani_skupin(ctyrky_zeny)
turnaj_zeny.rozlosovani_skupin(petky_zeny)
turnaj_zeny.rozlosovani_skupin(sestky_zeny)
    

