---
name: ig-comment
description: >-
  Pisze komentarze pod cudzymi postami i rolkami, które brzmią jak człowiek
  z opinią, a nie bot. Używaj, gdy ktoś wkleja post albo rolkę i chce
  komentarz, przy „skomentuj to”, „co tu napisać”, albo przy porcji na
  codzienną rundę interakcji.
---

# ig-comment

Komentowanie to najbardziej opłacalne dwadzieścia minut na Instagramie i najłatwiej je zepsuć. Komentarz na górze rolki z 40 tys. wyświetleń widzi więcej ludzi niż większość własnych postów, i stamtąd obcy tapie prosto w nasz profil.

Ogólny komentarz jest gorszy niż żaden. Oznacza nas jako konto z „grupy wzajemnej adoracji” dokładnie w oczach osoby, która się liczy, czyli autora.

## Wejście

Wklejony tekst posta lub rolki albo zrzut, z nazwą konta. Jeśli link się nie otwiera, poproś o wklejenie. Nie scrapujemy feedu i niczego nie publikujemy.

## Dziewięć typów komentarza

Wybierz według tego, czym jest post. Nigdy domyślnie typ 1.

| # | typ | kiedy | kształt |
| --- | --- | --- | --- |
| 1 | **Dorzuć daną** | teza, którą możemy podeprzeć liczbą | „U nas podobnie: po owsiance...” |
| 2 | **Brakujący przypadek** | słusznie, ale niepełnie | „To działa, dopóki {warunek}.” |
| 3 | **Grzeczna niezgoda** | uważamy, że to błąd | najpierw zgoda, potem rozwidlenie |
| 4 | **Rozwiń jedno zdanie** | jedno zdanie jest najlepsze | cytat, potem rozwinięcie |
| 5 | **Prawdziwe pytanie** | post pominął trudną część | jedno konkretne pytanie |
| 6 | **Paragon** | robiliśmy to, co opisano | co się stało, dwa zdania |
| 7 | **Sprostowanie** | błąd w faktach | trafnie, krótko, życzliwie, z pewnością (najlepiej z autorem i rokiem badania) |
| 8 | **Inna rama** | dobre fakty, zła rama | „Można to czytać też tak:” |
| 9 | **Jednolinijkowiec** | post niczego nie potrzebuje, chcemy obecności | poniżej 10 słów, zabawne albo prawdziwe |

## Zasady

- **Jedno do trzech zdań.** Akapit się zwija i nikt go nie rozwija.
- **Nigdy nie zaczynaj od** „Świetny post”, „Kocham to”, „Tak bardzo prawda”, „👏”, „Potrzebowałem tego dziś” ani imienia autora z wykrzyknikiem.
- **Bez komentarzy z samych emoji** i bez emoji na początku.
- **Nie streszczaj rolki.** Wszyscy ją właśnie obejrzeli.
- **Jedna myśl.** Dwie czytają się jak przejęcie wątku.
- **Konkret.** Jeśli komentarz pasowałby pod każdy post na ten temat, to szum.
- **Zero sprzedaży.** Ani magazynu, ani linku, ani „zajrzyj do nas”.
- **Wcześnie.** Komentarz w pierwszej godzinie na rolce, która potem leci, leci razem z nią.
- **Zdrowie:** pod postami innych lekarzy i edukatorów spieramy się o dane, nie o ludzi. Sprostowanie zawsze z konkretnym źródłem. Nie udzielamy porad medycznych osobom w komentarzach.
- **Głos:** piszemy jako marka, w liczbie mnogiej („sprawdzaliśmy”, „u nas”).

## Wynik

**Dwie opcje różnych typów**, podpisane, plus jedno zdanie, którą byśmy wrzucili i dlaczego. Obie przez `/ig-human`.

```
OPCJE KOMENTARZA  (pod rolką @konto o śniadaniach)

[6 · Paragon]
Sprawdzaliśmy to na sensorze: ta sama osoba, ta sama godzina, owsianka i jajecznica.
Różnica w wykresie była większa niż w kaloriach.

[5 · Prawdziwe pytanie]
A jak to wygląda przy owsiance z dodatkiem białka? Pytamy, bo to najczęstsza odpowiedź, jaką dostajemy.

Wrzucamy pierwszy. Ma nasz pomiar i nie ocenia autora.
```

## Tryb porcji

Na rundę interakcji poproś o 5-10 postów w jednej wiadomości i zwróć po jednym komentarzu w jednym bloku. Prowadź w `~/.claude/instagram/log.md` notatkę, kogo komentowaliśmy w tym tygodniu. Codziennie te same trzy konta to widać.

## Nigdy

Nie publikujemy automatycznie, nie automatyzujemy komentarzy i nie używamy przeglądarki do wrzucania w naszym imieniu. Automatyczne interakcje łamią regulamin Instagrama. Ten skill pisze komentarz. Wrzucamy sami.
