---
name: ig-canva
description: >-
  Robi gotowy post albo karuzelę w Canvie: od tematu do projektu 1080x1350 w
  naszym stylu, z linkiem do edycji, plikami PNG i opisem. Używaj przy „zrób
  post w Canvie”, „grafika na Instagram”, „wrzuć to do Canvy”, „zrób z tego
  projekt”, albo gdy tekst karuzeli jest zaakceptowany i trzeba go złożyć.
  Wymaga podłączonego connectora Canva.
---

# ig-canva

Agent od postów. Bierze temat albo gotowy tekst i oddaje projekt w Canvie, który można otworzyć, poprawić i pobrać. Pisanie zostawia skillom, które robią to dobrze. Sam składa.

**Nic nie jest publikowane.** Projekt ląduje na naszym koncie Canvy jako nowy plik. Istniejących projektów nie ruszamy.

## Zanim zaczniesz

1. Sprawdź, czy w sesji są narzędzia Canvy (`generate-design`, `copy-design`, `edit-design`, `export-design`). Jeśli nie ma, powiedz to wprost i oddaj tekst slajdów oraz pliki z `/ig-carousel` (HTML do PNG). Nie udawaj, że projekt powstał.
2. Przeczytaj `~/.claude/instagram/voice.md` i `~/.claude/instagram/canva.md`, jeśli są. W `canva.md` jest ID brand kitu, ID projektu-wzorca i opis naszego stylu. Wzór leży w `templates/canva.md`.
3. Przeczytaj `wzorce.md` z tego folderu. To pięć układów, które u nas mają największy zasięg, z liczbami. Każdy nowy post dostaje jeden z nich. Nazwij go przy tekście („wzorzec 3”) i powiedz, dlaczego ten.
4. Jeśli `canva.md` nie ma: `list-brand-kits` (jeden kit = bierzemy go, kilka = pytamy raz) i `search-designs` z frazą „Instagram”, żeby znaleźć projekt, z którego bierzemy wzór. Zapisz wynik do `canva.md`, żeby nie pytać drugi raz.

## Krok 1: tekst

Projekt bez zaakceptowanego tekstu to strata czasu, bo każda poprawka słowa oznacza przesuwanie pól.

- Jest tylko temat: karuzela idzie przez `/ig-carousel`, pojedyncza grafika to okładka z tego samego skilla (hook do 6 słów i jedna linia pod spodem).
- Jest gotowy tekst: sprawdź go zasadami z `/ig-carousel` (25 słów na slajd, numeracja, handle, slajd ze źródłami przy danych).
- Zawsze: `/ig-human` na tekście slajdów i warstwa zdrowotna. Bez „wyleczysz”, bez gwarancji, liczba tylko ze źródłem na slajdzie.

Przy wzorcach 1 i 2 z `wzorce.md` na grafice nie ma tekstu. Wtedy „tekst” to wybór zdjęcia i pierwsze zdanie opisu, które nazywa to, co widać.

Pokaż tekst jako numerowaną listę i poczekaj na „tak”. Dopiero potem Canva.

## Zdjęcia

Najlepsze posty stoją na prawdziwym zdjęciu, nie na grafice ze stocka.

**Nie powtarzamy zdjęć.** Zdjęcie, które siedzi już w którymś projekcie w Canvie, najpewniej było opublikowane. Z projektu-wzorca kopiujemy układ, a zdjęcie zawsze podmieniamy (`update_fill`). Jeśli po kopii na stronie zostało stare zdjęcie, post nie jest gotowy.

Szukaj w tej kolejności:

1. Zdjęcie, które dostaliśmy w rozmowie.
2. Dysk Google: foldery z `canva.md`. Pokaż dwa, trzy do wyboru. Plik wgraj do Canvy (`create-upload-url`), dopiero potem na slajd.
3. Zdjęcie wygenerowane w Canvie (`generate-image`, proporcje 4:5), tylko jedzenie i przedmioty, nigdy ludzie, pacjenci ani objawy. W wyniku napisz wprost, że zdjęcie jest wygenerowane.
4. Nic nie pasuje: zaproponuj inny układ bez zdjęcia (wzorzec 4, slajd z samym tekstem) albo powiedz, jakie zdjęcie trzeba zrobić.

W `~/.claude/instagram/log.md` zapisuj nazwę użytego pliku, żeby nie wziąć go drugi raz.

Nie ma pasującego zdjęcia: powiedz, jakie trzeba zrobić (co w kadrze, z bliska, pion). Nie zastępuj go wygenerowanym.

## Krok 2: projekt

Dwie drogi. Pierwsza daje nasz wygląd, druga jest na start i na nowe układy.

### A. Z naszego wzorca (domyślnie, gdy w `canva.md` jest projekt-wzorzec)

1. `copy-design` z ID wzorca i `page_numbers` stron, których układ pasuje (okładka, slajd z treścią, CTA). Jedna strona wzorca na jeden slajd. Powstaje nowy projekt, wzorzec zostaje nietknięty.
2. `read-design` na kopii z `open_transaction: true` i polami `design_content`, `thumbnails`. Dostajesz `transaction_id` i identyfikatory pól tekstowych.
3. `edit-design` strona po stronie (`page_index` od 1): `replace_text` w istniejących polach, `update_title` na nazwę `IG RRRR-MM-DD temat`. Zdjęcie w tle podmieniaj przez `update_fill` tylko na zasób, który wskazaliśmy albo który jest już na koncie.
4. Każde wywołanie z `finalize: "keep_open"`. Po zmianach pokaż miniatury.
5. `finalize: "commit"` osobnym wywołaniem, bez operacji, dopiero po naszym „tak”. Jeśli jest „nie”, popraw albo `cancel`.

### B. Generowanie z brand kitem (gdy wzorca nie ma albo chcemy nowy układ)

1. `generate-design` z `design_type: "instagram_post"` (wychodzi 1080x1350) i `brand_kit_id`. Narzędzie nie zna rozmowy, więc w `query` musi być wszystko: dokładne teksty w cudzysłowach, „użyj dokładnie tych tekstów, nic nie dopisuj”, opis stylu z `canva.md`, podpis i numer slajdu.
2. Pokaż kandydatów z linkami. My wybieramy.
3. `create-design-from-candidate` z `job_id` i `candidate_id`. Dopiero to daje prawdziwe `design_id`. ID z linków podglądu nie są ID projektu.
4. Generator zwykle oddaje jedną stronę. Przy karuzeli wygeneruj okładkę, a resztę dołóż przez `edit-design` (`add_page`, `add_text`, `format_text`) w tym samym układzie, albo przejdź na drogę A.
5. Sprawdź polskie znaki i czy tekst nie został przepisany. Generator lubi dopisywać. Poprawki jak w A, punkty 2-5.

## Logo

Na każdym slajdzie jest nasze logo, bez wyjątku, także na okładce ze zdjęciem i na slajdzie z przepisem.

- Plik bierzemy z `canva.md` (ID zasobu w Canvie). Nie ma go tam: pytamy o plik, nie zgadujemy i nie rysujemy podobnego.
- Wstawiamy `insert_fill` i na tym koniec. Logo zostaje 1:1: bez zmiany kolorów (`recolor_element` zabronione), bez przycinania, bez obrotu, bez przezroczystości, bez efektów.
- Zmieniamy tylko rozmiar, zawsze z zachowaniem proporcji (`preserve_aspect_ratio: true`, jeden wymiar).
- W `canva.md` są dwa logo. Domyślne to twarze, pasuje na każde tło. Biały napis tylko na ciemne tło.
- Tekst dodany przez `add_text` dostaje domyślny krój Canvy. Nagłówki i treść bierzemy ze stron wzorca (opis w `canva.md`, „karta z tekstem”), żeby miały nasz krój. `add_text` zostaje na drobne rzeczy: numer slajdu, handle, źródło.
- To samo miejsce i ta sama wielkość na wszystkich slajdach, poza zewnętrznymi 60 px. Pod logo ma być spokojne tło. Jeśli zdjęcie jest w tym miejscu pstre, przesuwamy zdjęcie albo tekst, nie logo.

## Krok 3: kontrola przed oddaniem

Obejrzyj miniaturę każdej strony, nie zakładaj.

- Okładka czytelna w miniaturze 400 px. Jeśli trzeba mrużyć oczy, tekst jest za mały.
- Tekst poza zewnętrznymi 120 px, bo siatka profilu przycina.
- ą, ę, ł, ó, ś, ż, ź, ć, ń wyświetlają się poprawnie. Część fontów ich nie ma.
- Tekst na slajdzie zgadza się słowo w słowo z zaakceptowanym.
- Logo na każdej stronie, niezmienione, w tym samym miejscu.
- Żadnego zdjęcia, które było już w innym projekcie w Canvie.
- Numer slajdu i handle na każdej stronie. Źródła przy danych.
- Zdjęcia: bez „przed i po”, bez cudzych twarzy i wyników pacjentów bez zgody.

## Krok 4: pliki i opis

- `get-export-formats`, potem `export-design` jako PNG, wszystkie strony. Podaj linki do pobrania i kolejność plików.
- Opis przez `/ig-caption` (zadanie B), tekst alternatywny do okładki.
- Dopisz wiersz do `~/.claude/instagram/log.md`: data, temat, format, link do projektu.

## Wynik

```
POST W CANVIE  ·  karuzela, 8 stron, 1080x1350

Edycja:   https://www.canva.com/d/...
Pliki:    8 x PNG (linki ważne krótko, pobierzcie od razu)
Droga:    A, strony 1, 4, 4, 4, 4, 4, 9, 12 z wzorca

Do sprawdzenia przez Was:
- slajd 5: zdjęcie z wzorca, podmienić na własne
- slajd 7: {{źródło}} do liczby 38%

OPIS
...
ALT
...
```

## Czego nie robimy

- Nie publikujemy i nie planujemy. Wyjątek jak w `/ig-plan`: jeśli o to poprosimy i jest Metricool, gotowy post może trafić jako szkic **do akceptacji** (`createScheduledPostForReview`), po wyraźnym „tak”.
- Nie zapisujemy zmian w projekcie bez pokazania podglądu.
- Nie edytujemy wzorca ani żadnego starego projektu. Zawsze kopia.
- Nie używamy drugi raz zdjęcia, które jest już w Canvie.
- Nie oddajemy slajdu bez logo i nie zmieniamy logo.
- Nie generujemy zdjęć ludzi, pacjentów ani „efektów”. Wykres tylko z naszych danych.
- Nie zgadujemy stylu. Jeśli `canva.md` jest puste, a wzorca nie ma, pytamy o jeden post, który wygląda tak, jak ma wyglądać następny.
