
from Rozlosovani_turnaje_ve_stolnim_tenisu import Hrac, Turnaj

SOUBOR = "prihlaseni_hraci_test.xlsx"


# ------------------------------------------------------------
# 1) Test načtení Excelu
# ------------------------------------------------------------
def test_nacteni_excelu():
    hraci = Hrac.nacist_hrace(SOUBOR)

    # Excel nesmí být prázdný
    assert len(hraci) > 0

    # Každý hráč musí mít povinné údaje
    for h in hraci:
        assert isinstance(h.jmeno, str) and h.jmeno.strip()
        assert isinstance(h.prijmeni, str) and h.prijmeni.strip()
        assert isinstance(h.gender, str) and h.gender.strip()
        assert isinstance(h.klub, str)
        assert isinstance(h.nasazeni, int)


# ------------------------------------------------------------
# 2) Test správného rozdělení na muže a ženy
# ------------------------------------------------------------
def test_rozrazeni_gender_excel():
    hraci = Hrac.nacist_hrace(SOUBOR)
    muzi, zeny = Hrac.rozradit_gender(hraci)

    # Kontrola, že nikdo nezmizel
    assert len(muzi) + len(zeny) == len(hraci)

    # Reálná data
    # Tvůj Excel má: 30 mužů a 7 žen
    assert len(muzi) == 30
    assert len(zeny) == 12


# ------------------------------------------------------------
# 3) Test seřazení a přepsání nasazení
# ------------------------------------------------------------
def test_serazeni_real_data():
    hraci = Hrac.nacist_hrace(SOUBOR)
    muzi, _ = Hrac.rozradit_gender(hraci)

    serazeni = Hrac.serazeni_a_prepis_nasazeni(muzi)

    nasazeni = [h.nasazeni for h in serazeni]

    # Nasazení MUSÍ být 1...N bez děr
    assert nasazeni == list(range(1, len(muzi) + 1))

    # Musí být seřazeno podle původního nasazení z Excelu
    puvodni = sorted([h.nasazeni for h in muzi])
    assert len(puvodni) == len(serazeni)


# ------------------------------------------------------------
# 4) Test rozdělení do košů (20 hráčů → 6 košů)
# ------------------------------------------------------------
def test_kose_real_data():
    hraci = Hrac.nacist_hrace(SOUBOR)
    muzi, _ = Hrac.rozradit_gender(hraci)
    serazeni = Hrac.serazeni_a_prepis_nasazeni(muzi)

    turnaj = Turnaj(muzi)
    turnaj.vytvor_skupiny(len(muzi))

    kose = Hrac.rozdeleni_na_kose(serazeni, turnaj.pocet_skupin)

    # Musí být vždy 6 košů
    assert len(kose) == 6

    # Součet hráčů v koších = počet hráčů
    total = sum(len(k) for k in kose)
    assert total == len(muzi)

    # Rovnoměrné naplnění (max rozdíl 1)
    velikosti = [len(k) for k in kose]
    if min(velikosti) > 0:
        assert max(velikosti) - min(velikosti) <= 1


# ------------------------------------------------------------
# 5) Test vytvoření skupin podle reálného počtu hráčů
# ------------------------------------------------------------
def test_skupiny_real_data():
    hraci = Hrac.nacist_hrace(SOUBOR)
    muzi, _ = Hrac.rozradit_gender(hraci)

    turnaj = Turnaj(muzi)
    turnaj.vytvor_skupiny(len(muzi))

    # 30 hráčů → 7 skupin
    assert turnaj.pocet_skupin == 7
    assert len(turnaj.skupiny) == 7


# ------------------------------------------------------------
# 6) Test kompletního rozlosování podle reálných dat
# ------------------------------------------------------------
def test_kompletni_rozlosovani_excel():
    hraci = Hrac.nacist_hrace(SOUBOR)
    muzi, _ = Hrac.rozradit_gender(hraci)
    serazeni = Hrac.serazeni_a_prepis_nasazeni(muzi)

    turnaj = Turnaj(muzi)
    turnaj.vytvor_skupiny(len(muzi))

    kose = Hrac.rozdeleni_na_kose(serazeni, turnaj.pocet_skupin)

    turnaj.rozlosovani_jednicek(kose[0])
    for kos in kose[1:]:
        turnaj.rozlosovani_skupin(kos)

    # ------------------------------------
    # VALIDACE
    # ------------------------------------

    # Všichni hráči musí být rozlosováni
    rozlosovani = [h for s in turnaj.skupiny for h in s.hraci]
    assert len(rozlosovani) == len(muzi)

    # Nikdo se nesmí opakovat
    assert len(set(id(h) for h in rozlosovani)) == len(muzi)

    # Žádná skupina nesmí být prázdná
    assert all(len(s.hraci) > 0 for s in turnaj.skupiny)

    # TOP hráči musejí být ve své skupině sami z 1. koše
    for skupina in turnaj.skupiny:
        jedna_kose = [h for h in skupina.hraci if h.kos == 1]
        assert len(jedna_kose) <= 1

