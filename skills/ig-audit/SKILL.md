---
name: ig-audit
description: >-
  Analiza po fakcie tego, co już opublikowaliśmy: które rolki naprawdę
  zadziałały, dlaczego, i czego przestać robić. Używaj, gdy ktoś wkleja
  statystyki z Instagrama albo listę postów i pyta „co działa”, „czemu to nie
  poszło”, „przeczytaj nasze statystyki”, „zrób audyt treści”, albo chce
  wiedzieć, czego robić więcej.
---

# ig-audit

Jedynym uczciwym źródłem tego, co działa na koncie, jest to konto. Każda zasada w każdym poradniku, łącznie z tymi w tym pakiecie, to założenie. Nasze ostatnie 30 postów to dowód.

## Wejście

Najpierw sprawdź, czy w sesji jest connector **Metricool** albo **vidIQ** z danymi Instagrama (`getAnalyticsDataByMetrics`, `vidiq_instagram_owner_insights`). Jeśli tak, pobierz statystyki postów za ostatnie 8-12 tygodni stamtąd i zapisz do pliku, zanim zaczniesz liczyć. Jeśli nie, poproś o to, co mamy:

- Statystyki per post: wyświetlenia, zasięg, interakcje, czas oglądania, zapisania, udostępnienia, obserwacje, udział nie-obserwujących w zasięgu. Zrzuty są OK.
- Albo wykres utrzymania widzów dla najlepszej i najgorszej rolki. Ten jeden zrzut jest wart więcej niż reszta.
- Albo same posty z wyświetleniami, na pierwsze podejście wystarczy.

Przeczytaj też `~/.claude/instagram/log.md`, bo zapisuje, jakiej formuły użył każdy post.

Liczby liczymy kodem, nie w głowie: dane do pliku, obliczenia w Pythonie.

## Co mierzymy

Surowe wyświetlenia to najmniej użyteczna liczba, bo zależy głównie od tego, ilu ludzi już obserwuje. Policz to i pokaż obliczenia:

| miara | jak | co mówi |
| --- | --- | --- |
| **Mnożnik** | wyświetlenia / mediana naszych wyświetleń | prawdziwy hit czy zwykły dzień |
| **Zasięg poza obserwującymi** | % zasięgu od nie-obserwujących | czy w ogóle poleciało |
| **Utrzymanie po 3 s** | widzowie po 3 s / widzowie na starcie | czy hook zadziałał. To ocena hooka. |
| **Średni czas oglądania** | ze statystyk | czy zadziałał środek |
| **Udostępnienia na zasięg** | udostępnienia / zasięg | najsilniejszy sygnał. Ktoś podpisał się pod tym nazwiskiem. |
| **Obserwacje na zasięg** | obserwacje / zasięg | czy profil zamienił uwagę w obserwację |

Ranking po mnożniku i udostępnieniach na zasięg, nie po wyświetleniach.

## Wzorzec

Pięć najlepszych i pięć najgorszych obok siebie. Szukaj, co je dzieli, i bądź gotów na wniosek, który się nie spodoba:

- **Utrzymanie po 3 s.** Jeśli tu się różnią, to hook i nic innego.
- **Formuła hooka.** Które numery z `ig-reel/hooks.json` są w pierwszej piątce?
- **Format.** Rolka, karuzela, grafika.
- **Długość.** <15 s, 15-30, 30-60, >60.
- **Temat.** Np. mechanizm kontra krytyka badań kontra pytanie widza.
- **Kto jest na ekranie.** Jeden z braci, obaj, lekarz-gość, bez twarzy.
- **Czy odpowiadaliśmy na komentarze w pierwszej godzinie.**
- **Dzień i godzina.** Sprawdź **na końcu** i tylko jeśli reszta nic nie pokazuje. Prawie nigdy to nie jest przyczyna.

Wniosek jako twierdzenie z dowodem i poziomem pewności. Przy 30 postach widać wzorzec. Przy 6 nie, i lepiej to powiedzieć niż go wymyślić.

## Rozróżnienie, które oszczędza miesiące

**Rolka z wyświetleniami i bez obserwacji to nie porażka rolki, tylko problem profilu.** Rolka bez wyświetleń to problem hooka. Najpierw je rozdziel. Jeśli zasięg poza obserwującymi jest wysoki, a obserwacji na zasięg mało, przestań przepisywać hooki i idź do `/ig-profile`.

## Wynik

```
AUDYT  ·  31 postów  ·  12.08 - 05.11  ·  mediana wyświetleń 4 100

TOP 5 WG MNOŻNIKA
  18.2x  #17 Pojedynek     74 600 wyśw.  62% spoza  3s: 71%  128 udost.
  ...

DÓŁ 5
   0.3x  #11 Lista          1 200 wyśw.   9% spoza  3s: 31%    2 udost.

CO MÓWIĄ DANE
1. Utrzymanie po 3 s to cała historia. Top 5: średnio 66%, dół 5: 33%.
2. Rolki z naszym własnym pomiarem: średnio 8,1x vs 0,9x reszta. n=5. Najsilniejszy sygnał.
3. Listy „5 produktów” mają wyświetlenia i nic więcej. Trzy z dolnej piątki.
4. Dzień tygodnia nic nie pokazuje.

STOP: listy produktów.
WIĘCEJ: pomiary i porównania z liczbą.
```

(Liczby w przykładzie są ilustracją formatu.)

Potem przekaż wnioski do `/ig-plan`, żeby następny tydzień stał na naszych dowodach, i do `/ig-viral`, żeby swipe file filtrował formuły, które działają u nas.
