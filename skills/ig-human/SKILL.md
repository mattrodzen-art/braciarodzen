---
name: ig-human
description: >-
  Usuwa z tekstu ślady AI po polsku: pauzy (—), wypełniacze („kluczowy”,
  „warto podkreślić”, „w dzisiejszym świecie”), niewidoczne znaki, angielskie
  cudzysłowy, i ocenia wynik w pięciu testach. Flaguje też mgliste autorytety
  („badania pokazują” bez źródła). Używaj, gdy tekst ma brzmieć jak człowiek,
  przy „czy to brzmi jak AI”, „uczłowiecz”, „usuń wypełniacze”, oraz zawsze
  przed pokazaniem opisu, scenariusza, komentarza, odpowiedzi albo DM.
---

# ig-human

Dwa działające narzędzia. Używaj ich.

```bash
python3 humanize.py szkic.txt --report        # czyści i pokazuje zmiany
python3 humanize.py szkic.txt -o czysty.txt   # zapisuje wynik
python3 detect.py szkic.txt                   # ocena, pięć testów
python3 detect.py szkic.txt czysty.txt        # przed i po
```

Oba czytają `slop.json`: polski słownik wypełniaczy (przymiotniki we wszystkich formach, bo regex nie zna odmiany), frazy, blok instagramowy, niewidoczne znaki, typografię i 18 wzorców strukturalnych. Słownik powstał na bazie naszego skilla „Pisz jak człowiek”. Jest do edycji: jeśli jakieś słowo jest naprawdę nasze, usuń je z pliku.

## Co poprawia się samo

1. **Niewidoczne znaki.** Spacje zerowej szerokości, łączniki, miękkie dywizy, BOM, znaki tagów, twarde spacje. Klawiatura ich nie robi, a przetrwają kopiuj-wklej.
2. **Typografia.** Pauza (—) zamienia się na przecinek. Angielskie “ i proste "..." na polskie „...”. Wielokropek na trzy kropki. Półpauza ze spacjami ( – ) zostaje, bo to poprawny polski myślnik, ale używamy jej oszczędnie.
3. **Słownik.** „kluczowy” -> „ważny”, „odgrywa kluczową rolę” -> „ma znaczenie”, „w dzisiejszym świecie” -> usunięte, „warto podkreślić, że” -> usunięte, reklamowe przymiotniki („innowacyjny”, „holistyczny”, „wyjątkowy”) -> usunięte. Plus blok instagramowy: „przestań scrollować”, „w dzisiejszym filmie”, „obserwuj po więcej”, „oznacz kogoś, kto”.

## Czego skrypt nie poprawia

Wzorce strukturalne są **flagowane, nie przepisywane**, bo zmiana kształtu zdania wymaga oceny:

- „Nie tylko X, ale także Y”, „To nie X, to Y”, „Nie chodzi o X. Chodzi o Y.”
- reguła trzech, retoryczne „Efekt?” w osobnej linii
- „Podsumowując”, „Oto czego się nauczyliśmy”
- wstęp „w tym filmie pokażemy wam”, prośba o uwagę
- punkty z emoji, trzy słowa wielkimi literami, ściana hashtagów, ogólne przynęty
- **mgliste autorytety**: „badania pokazują”, „naukowcy odkryli”, „eksperci zalecają” bez wskazania którego badania. W naszej niszy to nie styl, to wiarygodność. Podaj autora i rok albo usuń.
- „stanowi”, „pełni funkcję” zamiast „jest”

Te linie przepisz ręcznie, zachowując sens, i uruchom `detect.py` jeszcze raz.

## Pięć testów

| test | co mierzy | maszyna wygląda tak |
| --- | --- | --- |
| RYTM | zmienność długości zdań | każde zdanie tej samej długości |
| KONKRET | liczby, nazwy, terminy (HbA1c, insulina) na 100 słów | abstrakcje, zero liczb |
| WYPEŁNIACZE | trafienia w słownik na 100 słów | „kluczowy”, „istotny”, „warto” |
| ODCISK | niewidoczne znaki, pauzy, nie-polskie cudzysłowy | typografia idealna co do znaku |
| GŁOS | formy osobowe („my”, „ty”, „-my”, „-sz”) kontra bezosobowe („należy”, „warto”, „zostało”) i wzorce | bezosobowo, z inscenizacją |

Werdykt to 60% średniej i 40% najsłabszego testu, bo jeden sygnał wystarczy. OK wymaga 70+ i żadnego testu poniżej 55. Pozostałe werdykty: DO POPRAWY, WYGLĄDA NA AI.

## Powiedz to uczciwie

To lokalne heurystyki. Działają na komputerze, nic nie jest wysyłane. To **nie** GPTZero ani żaden inny detektor i nie obiecują ich werdyktu. Polska wersja nie była testowana na dużym polskim korpusie. Nigdy nie mów, że tekst jest „niewykrywalny”.

## Kolejność

1. `humanize.py szkic.txt -o czysty.txt --report`
2. Przeczytaj flagi strukturalne i przepisz te linie sam.
3. `detect.py szkic.txt czysty.txt`, żeby pokazać przed i po.
4. Jeśli werdykt nie jest OK, popraw najsłabszy test i powtórz. Dwie rundy to norma. Pięć znaczy, że szkic był pisany według formułki i trzeba nowego szkicu.
5. Pokaż oczyszczony tekst razem z wynikiem. Nigdy samego wyniku.
