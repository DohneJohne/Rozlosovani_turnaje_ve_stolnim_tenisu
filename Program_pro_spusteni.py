from Rozlosovani_turnaje_ve_stolnim_tenisu import Hrac, Turnaj

#Volání tříd a metod pro správné nalosování turnaje
#--------------------------------------------------#
#Přečtení Excelu ze složky (pojmenování xlsx souboru zde a ve složce musí být shodné)
#("<Název excelu uloženého ve složce>.xlsx")
hraci = Hrac.nacist_hrace("prihlaseni_hraci_test.xlsx")

#Rozřazení hráčů dle genderu
muzi, zeny = Hrac.rozradit_gender(hraci)

#Přepis globálního nasazení na lokální
muzi = Hrac.serazeni_a_prepis_nasazeni(muzi)
zeny = Hrac.serazeni_a_prepis_nasazeni(zeny)

#Určení počtu hráčů
pocet_hracu_muzi = len(muzi)
pocet_hracu_zeny = len(zeny)

#Vytvoření turnaje pro muže a pro ženy
turnaj_muzi = Turnaj(muzi)
turnaj_zeny = Turnaj(zeny)

#Vytvoření daného počtu skupin dle počtu hráčů na turnaji
turnaj_muzi.vytvor_skupiny(pocet_hracu_muzi)
turnaj_zeny.vytvor_skupiny(pocet_hracu_zeny)

#Určení počtu skupin
pocet_skupin_muzi = turnaj_muzi.pocet_skupin
pocet_skupin_zeny = turnaj_zeny.pocet_skupin

#Rozdělení hráčů do košů (jedničky skupin, dvojky skupin...)
jednicky_muzi, dvojky_muzi, trojky_muzi, ctyrky_muzi, petky_muzi, sestky_muzi, sedmicky_muzi =Hrac.rozdeleni_na_kose(muzi, pocet_skupin_muzi)
jednicky_zeny, dvojky_zeny, trojky_zeny, ctyrky_zeny, petky_zeny, sestky_zeny, sedmicky_zeny =Hrac.rozdeleni_na_kose(zeny, pocet_skupin_zeny)

#Rozlosování všech hráčů do skupin
turnaj_muzi.rozlosovani_jednicek(jednicky_muzi)
turnaj_zeny.rozlosovani_jednicek(jednicky_zeny)
turnaj_muzi.rozlosovani_skupin(dvojky_muzi)
turnaj_muzi.rozlosovani_skupin(trojky_muzi)
turnaj_muzi.rozlosovani_skupin(ctyrky_muzi)
turnaj_muzi.rozlosovani_skupin(petky_muzi)
turnaj_muzi.rozlosovani_skupin(sestky_muzi)
turnaj_muzi.rozlosovani_skupin(sedmicky_muzi)
turnaj_zeny.rozlosovani_skupin(dvojky_zeny)
turnaj_zeny.rozlosovani_skupin(trojky_zeny)
turnaj_zeny.rozlosovani_skupin(ctyrky_zeny)
turnaj_zeny.rozlosovani_skupin(petky_zeny)
turnaj_zeny.rozlosovani_skupin(sestky_zeny)
turnaj_zeny.rozlosovani_skupin(sedmicky_zeny)

#Export skupin do Excelu ("<název vašeho turnaje>.xlsx")
turnaj_muzi.export_turnaje_do_excelu("muzi_skupiny.xlsx", skupin_na_list=4)
turnaj_zeny.export_turnaje_do_excelu("zeny_skupiny.xlsx", skupin_na_list=4)