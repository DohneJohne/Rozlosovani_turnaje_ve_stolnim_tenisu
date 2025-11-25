import pandas as pd
import random
from weasyprint import HTML

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
                min_pocet = min(len(s.hraci) for s in self.skupiny) #Při rovnosti hráčů ve více skupinách, program vybere náhodnou skupinu
                nejlepsi_skupiny = [s for s in self.skupiny if len(s.hraci) == min_pocet]
                cilova_skupina = random.choice(nejlepsi_skupiny)
        
            podskupinky_ze_zakladniho_rozlosovani.remove(hrac)
    
    def export_pdf_turnaje(self, vystup_pdf="turnaj.pdf", skupiny_na_stranku=4, nazev_turnaje= "Turnaj"):
            """
            Vygeneruje jeden PDF soubor se všemi skupinami v tomto turnaji.
            - vystup_pdf: výstupní cesta .pdf
            - groups_per_page: kolik skupin na jednu stránku (standardně 4)
            """
            #CSS - stará se o vzhled pdf, definice toho jak bude vypadat stránka
            css = """
            <style>
            @page { size: A4; margin: 18mm; }
            body { font-family: Arial, sans-serif; color: #000; }
            .page { width: 100%; display: block; page-break-after: always; }
            .group { width: 48%; display: inline-block; vertical-align: top; margin: 0.5%; box-sizing: border-box; }
            h2 { font-size: 16px; margin: 6px 0 8px 0; text-align: left; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 8px; }
            th, td { border: 0.7px solid #000; padding: 6px; text-align: center; font-size: 11px; }
            .namecell { text-align: left; font-size: 12px; }
            .clubsmall { font-size: 10px; color: #111; }
            /* zabrani rozsekani skupiny pres stranku */
            .group { page-break-inside: avoid; -webkit-column-break-inside: avoid; -moz-column-break-inside: avoid; }
            </style>
            """

            html = "<html><head>" + css + "</head><body>" #HTML určuje strukturu a obsah
            #Nadpis turnaje
            html += f"""
            <h1 style="text-align:center; font-size:26px; margin-bottom:10px;">
                {nazev_turnaje}
            </h1>
            <hr style="border:1px solid #000; margin-bottom:25px;">
            """
            #Vytvoření bloků skupin, tak aby na jednu stránku A4 připadalo group
            skupiny = self.skupiny
            kolik_je_skupin_na_strance = skupiny_na_stranku
            
            #Podle počtu skupin na stránku se rozdělí skupiny do tohoto počtu (např.10 skupin bude na třech stránkách (4+4+2))
            for zacatek_stranky in range(0, len(skupiny), kolik_je_skupin_na_strance):
                html += '<div class="page">'
                skupiny_na_strance = skupiny[zacatek_stranky:zacatek_stranky + kolik_je_skupin_na_strance]
                
                #Vytvoření tabulky pro skupinu a její celkové vyplnění informacemi
                for skupina in skupiny_na_strance:
                    hraci = skupina.hraci
                    n = len(hraci)
                    #Název skupiny
                    html += f"<div class='group'><h2>Skupina {skupina.id_skupiny}</h2>"
                    #Tabulka: první prázdná buňka + jména v hlavičce
                    html += "<table>"
                    html += "<tr><th></th>"
                    for h in hraci:
                        #Jméno (nasazení) a pod tím menším písmem klub
                        html += ("<th style='font-weight:normal;'>"
                                f"{h.jmeno} {h.prijmeni}<br>({h.nasazeni})<br>"
                                f"<span class='clubsmall'>{h.klub}</span>"
                                "</th>")
                    html += "</tr>"

                    #Řádky: vlevo jméno + buňky (diagonála X)
                    for i, hrac_radek in enumerate(hraci):
                        html += ("<tr>"
                             f"<th class='namecell'>{hrac_radek.jmeno} {hrac_radek.prijmeni} "
                             f"({hrac_radek.nasazeni})<br><span class='clubsmall'>{hrac_radek.klub}</span></th>")
                        for j in range(n): #Pokud se shoduje i-tý řádek a j-tý sloupec, tak vykreslí "X"
                            if i == j:
                                html += "<td><strong>X</strong></td>"
                            else:
                                html += "<td></td>"
                        html += "</tr>"

                    html += "</table></div>"  #Konec skupiny

                html += "</div>"  #Konec stránky

            html += "</body></html>"

            # vytvořit PDF
            HTML(string=html).write_pdf(vystup_pdf)
            print(f"PDF vytvořen: {vystup_pdf}")


#Volání tříd a metod pro správné nalosování turnaje
hraci = Hrac.nacist_hrace("prihlaseni_hraci_test.xlsx")
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
turnaj_muzi.export_pdf_turnaje(vystup_pdf="turnaj_muzi.pdf", skupiny_na_stranku=4,nazev_turnaje="Krajské přebory 2024")
turnaj_zeny.export_pdf_turnaje(vystup_pdf="turnaj_zeny.pdf", skupiny_na_stranku=4,nazev_turnaje="Krajské přebory 2024")

