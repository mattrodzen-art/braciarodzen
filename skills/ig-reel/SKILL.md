---
name: ig-reel
description: >-
  Zamienia surowy pomysł w rolkę na Instagram: trzy hooki z 26 formuł z oceną,
  scenariusz mówiony, napisy na ekran i rozpiskę ujęć z czasami, w głosie Braci
  Rodzeń. Używaj, gdy ktoś chce rolkę, reelsa, krótki film, hook, voiceover,
  „zrób rolkę o X”, „co powiedzieć w tym filmie”, albo ma zaraz nagrywać i nie
  ma pierwszego zdania. Also triggers on "reel", "short-form script", "hook".
---

# ig-reel

Jeden pomysł zamienia w rolkę, którą ktoś obejrzy do końca.

W tym folderze są dwa działające narzędzia. Używaj ich, nie oceniaj hooka na oko i nie zgaduj długości.

```bash
python3 hookscore.py hooki.txt              # ranking hooków
python3 hookscore.py --hook "jedno zdanie"  # ocena jednego
python3 beats.py scenariusz.txt --target 30 # rozpiska ujęć z czasami
```

Domyślne tempo to 140 słów na minutę (polskie słowa są dłuższe niż angielskie). Jeśli w voice.md jest zmierzone tempo, podawaj je przez `--wpm`.

## Zanim zaczniesz pisać

1. Przeczytaj `~/.claude/instagram/voice.md` (w claude.ai: jego treść z instrukcji projektu albo z wiadomości). To profil głosu: jak mówimy do kamery, czego nigdy nie mówimy, do kogo mówimy, jakie mamy granice w treściach zdrowotnych. Jeśli pliku nie ma, poproś o trzy nasze rolki albo opisy, wywnioskuj głos i zapisz plik na podstawie `templates/voice.md` z wtyczki. Scenariusz w cudzym głosie jest bezużyteczny, bo trzeba go powiedzieć na głos.
2. Przeczytaj `hooks.json` z tego folderu: 26 formuł, każda z szablonem, przykładem, wersją na ekran, przeznaczeniem i typową pułapką. Przykłady pokazują kształt. Liczby w przykładach nie są faktami do publikacji.
3. Jeśli pomysł jest cienki, nie pompuj go. Zadaj jedno zbiorcze pytanie: co się wydarzyło, komu, i ile to kosztowało albo dało. Rolka potrzebuje jednej konkretnej, prawdziwej rzeczy.
4. Jeśli istnieje `~/.claude/instagram/swipe.md` (pisze go `/ig-viral`), przeczytaj go. To nasze własne dowody, które formuły działają teraz w niszy. Mają pierwszeństwo przed domyślnymi.

## Kształt

Rolka rozstrzyga się w pierwszych dwóch sekundach, a utrzymuje w kolejnych pięciu.

```
0:00 - 0:02   HOOK        teza. Zdanie mówione i napis na ekranie, pisane osobno.
                          Ruch w pierwszej klatce, nie statyczna twarz.
0:02 - 0:07   STAWKA      dlaczego to ważne dla widza. Jedno zdanie.
0:07 - ...    TREŚĆ       jedna myśl na ujęcie, obraz zmienia się co ujęcie.
OSTATNIE 3s   NAGRODA     dowieź obietnicę z hooka, potem jedna prośba.
OSTATNIE ZDANIE PĘTLA     powtórz słowo z hooka, żeby replay wszedł gładko.
```

Długość robocza: 15 do 45 sekund. Rolki mogą mieć 3 minuty i prawie nikt nie powinien z tego korzystać.

## Pętla pracy

**1. Trzy hooki, nie jeden.** Wybierz trzy formuły z `hooks.json`, które naprawdę pasują do pomysłu. Do każdej napisz zdanie mówione i napis na ekran. Różne formuły, nie trzy przeróbki jednej.

**2. Oceń je.** Trzy zdania mówione do pliku, jedno w linii, `hookscore.py`. Pokaż ranking. Jeśli najlepszy ma poniżej 50, nie macie jeszcze hooka i żadna poprawka tego nie naprawi.

**3. Scenariusz** na zwycięskim hooku. Prosty język mówiony, tak jak naprawdę mówimy. Krótkie linie. Żadnego zdania, które trzeba ćwiczyć.

**4. Zmierz czas.** `beats.py scenariusz.txt --target {długość}`. Popraw każdą flagę: hook dłuższy niż 3 s, ujęcie ponad 4 s, kilka ujęć bez konkretu, brak pętli. Powtarzaj, aż będzie czysto.

**5. Uczłowiecz.** Przepuść scenariusz przez `/ig-human`. Zdanie, które brzmi jak pisane, słychać od razu, gdy ktoś je powie.

**6. Wydrukuj blok.** Scenariusz w bloku kodu, napisy na ekran osobno z czasami, potem:

```
ROLKA GOTOWA
hook:       #3 Nikt ci nie mówi, ocena 86 MOCNY
długość:    28,4 s, 9 ujęć, 140 sł/min
napisy:     6 plansz
humanizer:  4 ślady usunięte, wynik 81 OK
zdrowie:    bez obietnic, liczby z naszego pomiaru / {{źródło}}
opis:       teraz /ig-caption

Napisz „tak”, żeby zapisać w logu, albo co zmienić.
```

**7. Nigdy nie publikuj.** Ten skill pisze scenariusz. My nagrywamy i publikujemy. Po „tak” dopisz do `~/.claude/instagram/log.md` datę, numer formuły i pierwsze zdanie, żeby `/ig-audit` miał historię.

## Napisy na ekranie to osobny scenariusz

- **Najwyżej sześć słów na planszę.** Czyta je ktoś, kto jeszcze nie słucha.
- **Plansza z hookiem od klatki 1**, nie po sekundzie ciszy.
- **Strefa bezpieczna.** Na 1080x1920 nic powyżej y=230 i poniżej y=1440, prawe 230 px wolne. Resztę zakrywa interfejs.
- **Hook nigdy na dole kadru**, bo tam jest opis.
- **Napisy do całej treści.** Większość ogląda najpierw bez dźwięku.

## Zasady, które robią różnicę

- **Jedna myśl na rolkę.** Jeśli scenariusz ma dwie, to są dwie rolki. Powiedz to.
- **Liczby zamiast przymiotników.** „160 mg/dl” zamiast „bardzo wysoko”. Jeśli nie znamy liczby, zapytaj zamiast pisać wokół dziury.
- **Bez wstępu.** Bez powitania, bez „w tym filmie”, bez logo na start.
- **Zmiana kadru co ujęcie.** Statyczny kadr przez 8 sekund to moment wyjścia.
- **Jedna prośba na koniec.** Słowo-klucz w komentarzu, zapisz albo obserwuj. Jedna.
- **Niczego nie zmyślamy.** Żadnych wymyślonych pomiarów, pacjentów, wyników. Gdy liczba jest potrzebna i nieznana, zostaw `{{wasza liczba}}` i oflaguj.

## Zdrowie: granice

- Bez obietnic wyleczenia i gwarancji efektu („wyleczysz”, „gwarantujemy”, „cudowny”). `hookscore.py` traktuje to jako dyskwalifikację.
- Badanie przywołujemy tylko z nazwy (autor, rok) i tylko gdy je mamy. Inaczej `{{źródło}}`.
- Nie mówimy widzowi, żeby odstawił leki albo zmienił dawki. Jeśli temat dotyka leczenia, w scenariuszu pada „z lekarzem”.
- Cudzy wynik (pacjent, uczestnik) tylko za zgodą i z prawdziwymi liczbami.

## Przykład

```
/ig-reel po owsiance glukoza skacze bardziej niż po jajecznicy, sprawdzaliśmy sensorem
```

```
HOOKI (z oceną)
  80  MOCNY  #17 Pojedynek       „Owsianka kontra jajecznica. Sprawdziliśmy, co bardziej podnosi glukozę.”
                                 ekran: OWSIANKA VS JAJKA
  78  MOCNY  #22 Odwrócone       „Najważniejszy posiłek dnia? Dla twojej glukozy najgorszy.”
                                 ekran: NAJWAŻNIEJSZY POSIŁEK?
  51  OK     #6  Paragon          „Dwa tygodnie z sensorem. Tak wygląda glukoza po owsiance.”
                                 (brak stawki: nic nie jest na szali)

Nagrywamy #17: porównanie widać na wykresie i liczby są nasze.
Wersja #22 ma mocniejszy adres do widza, ale uogólnia. Zostawiamy ją na rolkę-opinię.
```
