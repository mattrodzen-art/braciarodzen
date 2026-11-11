---
name: ig-viral
description: >-
  Szuka rolek, które naprawdę działają teraz w naszej niszy, układa je według
  tego, jak bardzo pobiły własne konto, nazywa formułę hooka i robi z tego
  swipe file do nagrywania. Używaj przy „znajdź viralowe rolki”, „co teraz
  działa”, „co publikuje konkurencja”, „rozłóż to konto na części”, „zrób swipe
  file”, „czemu ta rolka tyle robi”, albo gdy nie wiemy, co nagrać dalej.
---

# ig-viral

Skill badawczy. Reszta pakietu pisze, ten patrzy. Raz w miesiącu, nie codziennie. Formuły żyją sezon.

```bash
python3 swipe.py zebrane.tsv --out ~/.claude/instagram/swipe.md
```

## Jedna myśl, dla której warto to robić

**Surowe wyświetlenia nie są dowodem.** Konto z dwoma milionami obserwujących i 400 tys. wyświetleń miało spokojny wtorek. Konto z czterema tysiącami i 400 tys. coś znalazło, i to da się skopiować.

Ranking po **mnożniku**: wyświetlenia podzielone przez medianę tego konta z ostatnich rolek. Ponad 3x to sygnał. Poniżej 1,5x to zwykły dzień konta i niczego nie uczy.

Zbieramy konta **w granicach około 10x naszego rozmiaru**.

## Krok 1: wybór kont

Poproś o 6-12 kont albo zaproponuj i poczekaj na akceptację:

- **4 bezpośrednie** - ta sama nisza (zdrowie metaboliczne, low carb, insulinooporność), trochę przed nami. Polskie i zagraniczne.
- **4 sąsiednie** - inna nisza, ta sama publiczność (fitness, gotowanie, rodzicielstwo, medycyna ogólnie). Stąd pożycza się formaty, zanim ktoś w niszy je ma.
- **2-4 duże** - tylko po format, nigdy po częstotliwość i ton.

Poproś też o otwarcie naszej kolekcji **Zapisane**. To najszybszy korpus, już przefiltrowany naszym gustem.

## Krok 2: oglądanie

Najpierw sprawdź, czy w sesji jest connector **vidIQ** z narzędziami Instagrama (`vidiq_ig_profile`, `vidiq_ig_profile_reels`, `vidiq_instagram_tiktok_outlier_search`). Jeśli tak, użyj go: daje wyświetlenia i liczby obserwujących bez logowania się gdziekolwiek. Jeśli nie, użyj przeglądarki dostępnej w sesji, z nami przy komputerze, albo poproś o wklejenie.

**Zasady bez negocjacji:**

- **Nigdy nie logujemy się na Instagram w czyimś imieniu i nie prosimy o hasło.**
- **To czytanie, nie scrapowanie.** Dziesięć kont, kilkanaście rolek każde, ludzkim tempem. Bez crawlera, bez usług do scrapowania, bez pętli w tle. Masowe zbieranie łamie regulamin i kończy się blokadą.
- **Kopiujemy formułę, nigdy film.** Kształt hooka, strukturę, długość, rytm cięć. Nie ich scenariusz, głos ani montaż. Każdy wiersz podpisany kontem, z którego pochodzi.
- **Nie kopiujemy twierdzeń zdrowotnych.** Rolka, która robi zasięgi na fałszywej obietnicy, jest przykładem formatu, nie treści. Zaznacz ją w uwagach.

**Co zapisujemy dla każdej rolki:** konto, obserwujący, mediana (środkowa liczba wyświetleń z ostatnich 12 rolek), wyświetlenia, hook (pierwsze zdanie, dosłownie, z błędami), pierwszy napis, długość, prośba na końcu. Mediana jest najważniejsza.

**Gdy Instagram nie pokazuje dość:** ta sama gramatyka hooków działa w YouTube Shorts, gdzie liczby i napisy są publiczne. Mamy też własny kanał na YouTube. Jeśli jest vidIQ, użyj go do Shorts; jeśli jest `yt-dlp`:

```bash
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J "https://www.youtube.com/@KANAL/shorts" > kanal.json
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "pl.*" --sub-format json3 -o hook "https://www.youtube.com/watch?v=ID"
```

Słowa z napisów z czasem poniżej 3,0 s to hook, tak jak został powiedziany.

## Krok 3: ranking

Plik TSV z nagłówkiem (nazwy kolumn po angielsku):

```
account	followers	median	views	hook
@konto	48000	11000	412000	nikt ci nie powie, że sok to cukier w szklance
```

`swipe.py` liczy mnożnik, nazywa formułę (te same 26 co w `/ig-reel`), ocenia hook i pokazuje, co odróżnia górną trzecią od dolnej.

## Krok 4: co to znaczy, ostrożnie

Trzy rzeczy i nic więcej:

1. **Które formuły są nadreprezentowane** w górnej trzeciej, z liczbami. Dwie formuły po cztery razy w sześciu kontach to wniosek. Jedna dwa razy to nie.
2. **Co strukturalnie łączy górną trzecią**: długość hooka, czy nagroda jest wizualna, czy pierwsza klatka się rusza, gdzie jest prośba.
3. **Wiersze „bez formuły”.** Przeczytaj je ręcznie. To szum albo formuła, której nie ma w `hooks.json`. Najcenniejsza kolumna.

Podaj wielkość próbki i pewność wprost. Czterdzieści rolek z sześciu kont coś mówi. Dwanaście nie.

## Krok 5: nasza wersja

Dla trzech najlepszych formuł napisz **naszą wersję**: nasza historia, nasza liczba, w działającym kształcie. Przekaż każdą do `/ig-reel` z wybranym numerem formuły. Nigdy „zróbcie coś jak to”. Zawsze zdanie, które możemy powiedzieć jutro.

## Wynik

```
SWIPE  ·  38 rolek  ·  7 kont  ·  odniesienie: mediana konta

NAD 3x
  38.4x  hook 86  #3  Nikt ci nie mówi   @konto_a   412 000  (mediana 10 700)
  ...

CO DZIAŁA
  #3 Nikt ci nie mówi   x5 w górnej trzeciej, 0 w dolnej
  mediana długości hooka: 7 słów u góry, 16 na dole

BEZ FORMUŁY (6)
  Dwa mają ten sam kształt: hook to przeczytany na głos komentarz widza.

NASZA WERSJA
  #3  „Nikt ci nie powie, że owsianka „fit” podnosi glukozę jak drożdżówka.” ({{nasz pomiar}})
```

Zapisz do `~/.claude/instagram/swipe.md`. Ten skill niczego nie publikuje, nie obserwuje, nie lajkuje i nie wysyła. Czyta.
