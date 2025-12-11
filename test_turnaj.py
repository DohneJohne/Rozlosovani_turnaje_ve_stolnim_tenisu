from Rozlosovani_turnaje_ve_stolnim_tenisu import Hrac, Turnaj


# ---- Pomocné funkce pro testy ----

def vytvor_test_hrace():
    data = [
        ("Jan", "Novak", "M", 3, "A"),
        ("Petr", "Svoboda", "M", 1, "B"),
        ("Karel", "Dvorak", "M", 2, "A"),
        ("Lucie", "Kralova", "F", 5, "C"),
        ("Eva", "Pokorna", "F", 4, "B"),
    ]

    hraci = [Hrac(jmeno=j, prijmeni=p, gender=g, nasazeni=n, klub=k) 
             for j,p,g,n,k in data]

    return hraci


# ---- TESTY ----

def test_rozrazeni_gender():
    hraci = vytvor_test_hrace()
    muzi, zeny = Hrac.rozradit_gender(hraci)

    assert len(muzi) == 3
    assert len(zeny) == 2
    assert all(h.gender.lower() in ["m", "muž"] for h in muzi)
    assert all(h.gender.lower() in ["f", "ž", "žena"] for h in zeny)


def test_serazeni_a_prepis_nasazeni():
    hraci = vytvor_test_hrace()
    muzi, zeny = Hrac.rozradit_gender(hraci)

    serazeni = Hrac.serazeni_a_prepis_nasazeni(muzi)

    nasazeni = [h.nasazeni for h in serazeni]
    assert nasazeni == [1, 2, 3]


def test_rozdeleni_na_kose():
    hraci = vytvor_test_hrace()
    muzi, zeny = Hrac.rozradit_gender(hraci)
    serazeni = Hrac.serazeni_a_prepis_nasazeni(muzi)

    jednicky, dvojky, trojky, *_ = Hrac.rozdeleni_na_kose(serazeni, pocet_skupin=1)

    assert len(jednicky) == 1
    assert len(dvojky) == 1
    assert len(trojky) == 1

    # Kontrola, že koš byl nastaven
    assert all(h.kos in [1,2,3] for h in serazeni)


def test_vytvoreni_skupin():
    hraci = vytvor_test_hrace()
    muzi, _ = Hrac.rozradit_gender(hraci)

    turnaj = Turnaj(muzi)
    turnaj.vytvor_skupiny(len(muzi))

    assert turnaj.pocet_skupin == 1
    assert len(turnaj.skupiny) == 1


def test_rozlosovani_jednicek():
    hraci = vytvor_test_hrace()
    muzi, _ = Hrac.rozradit_gender(hraci)
    serazeni = Hrac.serazeni_a_prepis_nasazeni(muzi)

    jednicky, *_ = Hrac.rozdeleni_na_kose(serazeni, pocet_skupin=1)

    turnaj = Turnaj(muzi)
    turnaj.vytvor_skupiny(len(muzi))
    turnaj.rozlosovani_jednicek(jednicky)

    assert len(turnaj.skupiny[0].hraci) == 1
    assert turnaj.skupiny[0].hraci[0].kos == 1


def test_rozlosovani_skupin():
    hraci = vytvor_test_hrace()
    muzi, _ = Hrac.rozradit_gender(hraci)
    serazeni = Hrac.serazeni_a_prepis_nasazeni(muzi)

    jednicky, dvojky, trojky, *_ = Hrac.rozdeleni_na_kose(serazeni, pocet_skupin=1)

    turnaj = Turnaj(muzi)
    turnaj.vytvor_skupiny(len(muzi))
    turnaj.rozlosovani_jednicek(jednicky)
    turnaj.rozlosovani_skupin(dvojky)
    turnaj.rozlosovani_skupin(trojky)

    assert len(turnaj.skupiny[0].hraci) == 3

    # Test že všichni hráči jsou přiřazení
    assert sorted(h.jmeno for h in turnaj.skupiny[0].hraci) == \
           sorted(h.jmeno for h in muzi)
