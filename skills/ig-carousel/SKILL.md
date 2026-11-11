---
name: ig-carousel
description: >-
  Buduje karuzelę na Instagram: okładkę, która zarabia przesunięcie, tekst
  slajd po slajdzie i pliki 1080x1350 do wrzucenia. Używaj przy „karuzela”,
  „slajdy”, „post do przesuwania”, „zrób z tego karuzelę”, albo gdy pomysł ma
  kształt listy lub kroków i zginąłby jako jedna grafika.
---

# ig-karuzela

Karuzela ma najdłuższy czas oglądania na siatce, bo przesunięcie to interakcja, a przewinięcie nie. Ma też drugą szansę: Instagram potrafi pokazać ją ponownie od dalszego slajdu komuś, kto za pierwszym razem nie zareagował. Dlatego slajd 2 też musi stać sam.

Format nagradza jedną myśl rozbitą na kroki. Karze opis pocięty na kawałki.

## Kiedy karuzela, a kiedy rolka

Karuzela, gdy pomysł ma **kolejność i trzeba go przeczytać drugi raz**: kroki, mechanizm (jak insulina, glukoza i wątroba grają razem), przed i po, lista do zrzutu ekranu, wyniki badań. Rolka, gdy jest ruch, twarz albo nagroda, którą trzeba zobaczyć.

Jeśli pomysł to jedna teza, przekaż go `/ig-reel` i powiedz dlaczego.

## Struktura

6 do 10 slajdów. Limit to 20 i 20 to książka, której nikt nie skończy.

```
1         OKŁADKA   hook. Najwyżej 6 słów, czytelne w miniaturze. Pod spodem
                    jedna linia obietnicy.
2         STAWKA    dlaczego to ważne, jedno zdanie. To też druga okładka.
3 do N    JEDNA MYŚL NA SLAJD. Nagłówek 3-7 słów, pod nim najwyżej 25 słów.
N+1       PODSUMOWANIE  całość jako lista. Ten slajd ludzie zapisują i wysyłają.
OSTATNI   CTA       jedna akcja. Zapisz, słowo-klucz albo obserwuj.
```

Przy karuzeli z danymi naukowymi: ostatni lub przedostatni slajd to **źródła** (autor, rok, czasopismo), małą czcionką. To u nas standard, nie dodatek.

## Zasady tekstu

- **Okładka to 80% wyniku.** Sześć słów. Duże.
- **Projektuj pod przycięcie siatki.** Buduj 1080x1350 i trzymaj tekst okładki z dala od zewnętrznych 120 px.
- **Numeruj slajdy** (3/8). Gdy widać koniec, więcej ludzi do niego dociera.
- **Żaden slajd nie jest akapitem.** Ponad 25 słów to dwa slajdy.
- **Podsumowanie jest do wysłania.** Wysłania to najsilniejszy sygnał. Ma działać bez kontekstu.
- **Handle na każdym slajdzie**, mały, w rogu. Zrzuty ekranu podróżują bez nas.
- **Tekst alternatywny** przynajmniej do okładki.
- **Zdrowie**: wykresy i liczby tylko z naszych danych albo ze źródła podanego na slajdzie. Bez obietnic efektu.

## Pliki

1080x1350 (4:5), JPEG lub PNG. Zbuduj jako HTML, jedna `<section>` na slajd, `width:1080px; height:1350px`, jeden kolor akcentu, tekst nie mniejszy niż 32 px. Wyrenderuj każdy slajd do PNG (Chrome headless, Playwright albo to, co jest w sesji). Jeśli jest nasz system marki albo Canva z naszym brand kitem, użyj go i nie wymyślaj palety.

## Wynik

Najpierw tekst slajd po slajdzie jako numerowana lista, do przeczytania w dziesięć sekund i poprawienia, zanim cokolwiek się wyrenderuje. Potem **opis** (zadanie B z `/ig-caption`). Oba przez `/ig-human`. Pliki budujemy dopiero po akceptacji tekstu.

```
KARUZELA  ·  8 slajdów

1  OKŁADKA  OWSIANKA VS JAJKA
            Ta sama godzina, inny wykres.
2  STAWKA   Śniadanie ustawia glukozę do obiadu.
3           CO MIERZYLIŚMY
            Sensor, dwa poranki, te same warunki.
...
7  PODSUM.  Trzy rzeczy, które zmieniamy rano.
8  CTA      Napisz SENSOR, wyślemy instrukcję.

Opis: zadanie B, hook w linii 1, jedna prośba, 3 tagi.
```

Nic nie jest wrzucane. Publikujemy sami.
