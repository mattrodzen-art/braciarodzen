---
name: ig-profile
description: >-
  Ocenia profil na Instagramie w skali 100 według 12-punktowej rubryki (plus
  kontrola wiarygodności dla treści zdrowotnych) i przepisuje to, co traci
  punkty: pole imienia, bio, link, wyróżnione relacje, trzy przypięte posty,
  siatkę. Używaj przy „popraw profil”, „popraw bio”, „oceń nasz Instagram”,
  „dlaczego nas nie obserwują”, albo gdy ktoś wkleja profil i pyta, jak wygląda.
---

# ig-profile

Profil to nie witryna, którą się ogląda. To **ekran decyzji**, na który ktoś trafia z jednej rolki i daje mu około trzech sekund na jedno pytanie: czy jest tu więcej tego, i czy to dla mnie.

## Wejście

Poproś o wklejenie albo zrzut: pole imienia, handle, bio, dokąd prowadzi link, nazwy wyróżnionych relacji, co jest przypięte, pierwsze dziewięć okładek. Zrzut górnej części profilu i dwóch pierwszych rzędów siatki wystarczy.

Nie logujemy się na Instagram w niczyim imieniu.

## Ocena

Przeczytaj `rubric.json` z tego folderu. Dwanaście pozycji, 100 punktów, każda z opisem pełnej oceny i typowej porażki. Oceń każdą, pokaż tabelę, podaj sumę. Uczciwie: większość profili ląduje przy pierwszym podejściu w okolicach 30-40, a hojna ocena nikomu nie pomaga.

Osobno, bez punktów, oceń **wiarygodność zdrowotną**: czy widać, kto stoi za treściami (lekarze, PTLI, źródła), i czy w bio nie ma obietnicy wyleczenia.

```
OCENA PROFILU  38/100

  pole imienia     2/12   sama nazwa, żadnych słów, które ktoś wyszukuje
  bio, linia 1     3/12   trzy hasła i emoji
  przypięte        0/10   nic nie przypięte
  wyróżnione       2/8    „Różne”, „2024”
  ...
  wiarygodność     brak informacji, kto mówi
```

## Potem przepisz, w tej kolejności

Od największej straty punktów. Nie wszystko naraz, bo każde pole trzeba zmienić ręcznie.

**1. Pole imienia (30 znaków).** Pogrubiona linia pod zdjęciem, nie handle. To pole przeszukuje wyszukiwarka. Format: `{Nazwa} | {czym się zajmujemy, słowami z wyszukiwarki}`. Trzy opcje.

**2. Bio, linia 1.** Dla kogo to jest i co się zmienia. Nie stanowisko, nie przymiotniki, nie lista po kreskach. Reszta ze 150 znaków: jeden dowód albo jedna jasna oferta. W liczbie mnogiej, bez obietnic wyleczenia.

**3. Trzy przypięte.** Trzy różne zadania: najlepszy dowód, najjaśniejsze wyjaśnienie oferty (magazyn, Akademia), najlepsze przedstawienie nas. Najsilniejsza poprawka na całym profilu i zajmuje cztery tapnięcia.

**4. Wyróżnione relacje.** Cztery do sześciu, nazwane pytaniami odbiorców: Od czego zacząć, Badania, Magazyn, Kim jesteśmy, Pytania. Resztę usuń.

**5. Link.** Jeden cel zgodny z obietnicą bio. Dwa to już menu.

**6. Okładki siatki.** Pierwsze dziewięć w miniaturze. Okładki rolek wybrane, nie pierwsza klatka. Cztery słowa na okładce robią siatkę czytelną od jednego spojrzenia.

## Wynik

Tabela ocen, potem przepisane pola jako bloki do skopiowania w kolejności poprawek, każde przez `/ig-human`. Na koniec ponowna ocena i uczciwa różnica. Jeśli po przepisaniu wychodzi 84, a nie 98, mówimy 84 i co jest potrzebne do reszty (zwykle siatka, nawyk relacji i przypięty post, którego jeszcze nie ma). To nie jest przepisanie.

Ten skill niczego nie zapisuje na Instagramie. Każde pole zmieniamy sami.
