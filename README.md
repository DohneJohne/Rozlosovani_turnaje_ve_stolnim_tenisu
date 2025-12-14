# **Rozlosování turnaje ve stolním tenisu**

Tento projekt je pomocí Pythonu sestavený algoritmus pro **Rozlosování turnaje ve stolním tenisu**.

Obsahuje:

* **Import hráčů z předpřipraveného Excelu**
* **Rozřazení hráčů podle genderu do turnaje mužů a žen**
* **Přepis z globálního žebříčkového nasazení na lokální turnajové nasazení**
* **Několik funkcí na rozlosování hráčů do skupin dle jejich nasazení**
* **Export rozlosování do Excelu pro okamžitý tisk**

---

## **Požadavky**

Je nutné mít nainstalovaný Python ve verzi 3.7+. Dále je nutné mít ve složce s tímto projektem vytvořené virtuální prostředí pro instalaci knihoven (návody lze snadno dohledat online).

Knihovny, které je potřeba nainstalovat: **pandas**, **openpyxl**, **pytest**.

```bash
pip install pandas
pip install openpyxl
pip install pytest
```

Všechny požadavky jsou také uvedeny v souboru `requirements`. Pokud nainstalujete tyto tři knihovny ručně, ostatní se nainstalují automaticky.

---

## **Návod k použití**

V repozitáři se nacházejí tři Python programy:

* **Rozlosovani_turnaje_ve_stolnim_tenisu**
* **Program_pro_spusteni**
* **test_turnaj**

Dále dva Excel soubory:

* **prihlaseni_hraci**
* **prihlaseni_hraci_test**

### **Excelový soubor `prihlaseni_hraci`**

Tento dokument slouží jako šablona pro zadání hráčů účastnících se turnaje. Každý hráč má povinné údaje, které musí být vyplněny. Pokud použijete jiný formát Excelu, program nebude fungovat.

Každý hráč musí mít vyplněno:

* jméno
* příjmení
* klub
* nasazení dle žebříčku (číselná hodnota)
* gender

Pokyny:

* Pokud ve vašem turnaji nezáleží na nasazení, nastavte všem hráčům hodnotu **1**.
* Pokud nezáleží na genderu, nastavte všem jednotný gender.
* Pokud nezáleží na klubu, nastavte všem stejný libovolný text.

Povolené hodnoty genderu:

* Muži: **"m"**, **"muž"**
* Ženy: **"f"**, **"ž"**, **"žena"**

Ostatní sloupce jsou volitelné, ale každý musí obsahovat alespoň nějaký text. Hráč se nenačte, pokud nejsou splněny všechny povinné podmínky.

### **Použití programu**

Pokud máte připravený Excel, vložte jej do stejné složky, kde máte virtuální prostředí i tento projekt, a stáhněte programy:

* **Rozlosovani_turnaje_ve_stolnim_tenisu** (nemusíte otevírat)
* **Program_pro_spusteni** (hlavní soubor)

V souboru *Program_pro_spusteni*:

* V horní části se nastavuje název Excelu se seznamem hráčů – text v uvozovkách **musí být shodný** s názvem Excelu.
* Ve spodní části se nastavuje název vygenerovaného Excelu – text v uvozovkách lze libovolně změnit.

Po spuštění programu se v terminálu zobrazí hláška:

> **"Turnaj rozlosován! Vygenerovaný Excel je ve stejné složce, jako tento kód"**

---

## **Testovací soubory**

* **prihlaseni_hraci_test** – ukázkový správně vyplněný Excel
* **test_turnaj** – testuje, zda všechny funkce algoritmu fungují správně (vhodné použít při úpravách kódu).

Ukázková data v souboru *prihlaseni_hraci_test* jsou veřejně dostupná z webu České asociace stolního tenisu a jedná se o turnaj **Krajské přebory mužů a žen Královehradeckého kraje 2025**.

---

## **Funkce kódu**

Program:

1. Načte seznam hráčů z Excelu.
2. Rozdělí hráče podle genderu na muže a ženy.
3. Seřadí hráče dle globálního nasazení.
4. Určí lokální turnajové nasazení (od 1 do počtu hráčů).
5. Vytvoří odpovídající počet skupin dle počtu hráčů.
6. Rozřadí hráče do košů (jedničky, dvojky, trojky…).
7. Losuje hráče do skupin:

   * Hráči ze stejného koše **nikdy nejsou ve stejné skupině**.
   * Program se snaží zabránit tomu, aby hráči ze stejného klubu skončili v jedné skupině (pokud to ještě lze).
8. Vygeneruje výsledný Excel s rozlosovanými skupinami.

Výsledný Excel je přehledný a zobrazí skupiny v klasické tabulkové podobě vhodné k tisku.

---

## **Příklad správně vyplněného řádku v Excelu**

Níže je ukázka jednoho řádku, který by měl být v Excelu vyplněn správně:

| Jméno | Příjmení | Gender | Klub      | Nasazení |
| ----- | -------- | ------ | --------- | -------- |
| Petr  | Novák    | m      | TTC Praha | 7        |


