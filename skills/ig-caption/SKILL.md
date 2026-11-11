---
name: ig-caption
description: >-
  Pisze opis pod post lub rolkę na Instagram: linię, która przetrwa cięcie
  „... więcej”, treść, jedną prośbę, frazy wyszukiwania i do pięciu hashtagów,
  a potem sprawdza go linterem (w tym kontrola obietnic zdrowotnych). Używaj
  przy „napisz opis”, „opis do rolki”, „co dać w opisie”, pytaniach o hashtagi,
  albo gdy rolka lub karuzela jest gotowa i brakuje tekstu.
---

# ig-caption

Jedno działające narzędzie:

```bash
python3 caption.py opis.txt
python3 caption.py opis.txt --keywords "insulinooporność,glukoza po posiłku"
```

Rysuje opis tak, jak pokazuje go feed: pierwsze ~125 znaków w ramce, reszta za tapnięciem. Przeczytaj tę ramkę, zanim przeczytasz cokolwiek innego.

## Najpierw: jakie zadanie ma ten opis

**Zadanie A: rolka już złapała widza.** Rolka ma własny hook. Opis nie jest drugim hookiem. Jego praca to prośba, kontekst do prośby i słowa, po których ludzie szukają.

**Zadanie B: opis jest treścią.** Zdjęcie, grafika, karuzela. Tu pierwsza linia jest hookiem i działa jak hook rolki: konkretna, krótka, ucięta w napięciu, a nie w pół zdania podrzędnego.

Powiedz, które zadanie piszesz i dlaczego.

## Kształt

```
Linia 1     ~125 widocznych znaków. A: prośba, wprost. B: hook.
            Nigdy powitanie, hashtag ani emoji na pierwszym znaku.
Treść       krótkie akapity z pustą linią między nimi. Dwa do sześciu.
            Tu mieszkają frazy wyszukiwania.
Prośba      jedna. Słowo-klucz w komentarzu, zapisz albo napisz do nas.
Hashtagi    najwyżej pięć, w osobnej linii na dole, albo wcale.
```

Limit to 2200 znaków. Opis, który zarobi tapnięcie i da 600 znaków, wygrywa z takim, który da 1800.

## Hashtagi

Od 18 grudnia 2025 Instagram pozwala na najwyżej pięć hashtagów w poście i rolce. Hashtag to etykieta tematu, nie dźwignia zasięgu. Pięć konkretnych (#insulinooporność, #dietaniskowęglowodanowa), zero ogólnych (#fyp, #viral, #zdrowie, #motywacja). Linter flaguje ogólne.

## Frazy wyszukiwania ważą więcej niż hashtagi

Wyszukiwarka Instagrama czyta tekst opisu. Fraza, po której chcemy być znajdowani, idzie do opisu tak, jak wpisałby ją człowiek, w zwykłym zdaniu. Uwaga na odmianę: linter szuka dokładnego ciągu, więc jeśli fraza to „insulinooporność”, niech choć raz padnie w tej formie.

## Zasady

- **Bez linków w opisie.** Nie są klikalne. Link w bio, w stories albo w DM.
- **Jedna prośba.** Dwie to jak żadna.
- **Słowo-klucz musi dać się wpisać.** Jedno słowo, bez spacji i bez emoji, wypowiedziane też w rolce. „Napisz SENSOR” działa. „Napisz »chcę instrukcję«” nie.
- **Emoji oszczędnie**, zgodnie z naszym stylem. Linter flaguje ponad 1,5 na 100 znaków.
- **Piszemy w liczbie mnogiej**: „my”, „sprawdziliśmy”, „wyślemy”. Do czytelnika na „ty”.
- **Tekst alternatywny** do zdjęć i karuzel. 20 sekund pracy.

## Zdrowie

Linter ma dwa testy dla naszej niszy:

- **OBIETNICE (FAIL)**: „wyleczysz”, „gwarantujemy”, „cudowny”, „detoks”, „odstaw leki”. Opisz mechanizm albo realny przypadek.
- **ŹRÓDŁA (WARN)**: „badania pokazują” bez wskazania którego. Autor i rok, albo przeformułuj.

## Pętla

1. Wybierz zadanie A lub B i powiedz które.
2. Szkic.
3. `/ig-human`. Opisy są krótkie, więc wypełniacz jest tu głośniejszy niż gdziekolwiek.
4. `caption.py` z naszymi frazami. Napraw każdy FAIL. Każdy WARN rozstrzygnij na głos.
5. Blok do skopiowania, potem:

```
OPIS GOTOWY
zadanie:    A - rolka niesie hook
widoczne:   118 ze 125 znaków przed cięciem
prośba:     jedna, słowo-klucz SENSOR
hashtagi:   3
frazy:      „insulinooporność” w linii 3
linter:     GOTOWE
```

Nic nie jest publikowane. Wklejamy sami.
