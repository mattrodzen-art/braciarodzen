# Agent do Instagrama - wersja polska dla Braci Rodzeń

Trzynaście skilli dla Claude'a, które prowadzą konto na Instagramie po polsku. Oparte na darmowym pakiecie [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) (licencja MIT, Jake Schincariol), przetłumaczone i przerobione pod nasz język, nasz styl i treści zdrowotne.

**Nic nie jest publikowane bez nas.** Skille piszą. My publikujemy.

## Co jest inne niż w oryginale

- Wszystkie instrukcje po polsku, w naszym stylu: liczba mnoga, prosty język, mało emoji.
- Narzędzia w Pythonie rozumieją polski: odmianę słów, polskie liczebniki, polskie znaki, tempo mowy (domyślnie 140 słów/min zamiast 165).
- 26 formuł hooków napisanych od nowa po polsku, z przykładami z niszy zdrowia metabolicznego.
- Humanizer ma polski słownik wypełniaczy, oparty na naszym skillu „Pisz jak człowiek”, i zamienia cudzysłowy na polskie „”.
- Warstwa zdrowotna w każdym skillu, który pisze treści: bez obietnic wyleczenia, badania z nazwy, bez porad o lekach w komentarzach i DM, odesłanie do lekarza. Hook z „wyleczysz” albo „gwarantujemy” dostaje dyskwalifikację, a opis z taką frazą nie przechodzi lintera.
- Profil głosu (`templates/voice.md`) jest w dużej części wypełniony.
- Opcjonalne użycie connectorów, jeśli są podłączone: Metricool (najlepsze godziny, statystyki, szkic posta do akceptacji) i vidIQ (dane z Instagrama do researchu, transkrypcje YouTube).

## Instalacja

**Claude Code albo aplikacja desktop z wtyczkami:** rozpakujcie folder `instagram-agent-pl` i w Claude Code wpiszcie:

```
/plugin marketplace add /ścieżka/do/instagram-agent-pl
/plugin install instagram-agent-pl
```

Albo skopiujcie foldery `skills/ig-*` do `~/.claude/skills/`. Potem wpiszcie `/ig` i sprawdźcie, czy pojawia się lista komend.

**claude.ai (przeglądarka, aplikacja):** w folderze `claude-ai/` jest każdy skill jako osobny plik .zip, gotowy do dodania w ustawieniach Claude'a w sekcji skilli. Narzędzia w Pythonie działają tam w środowisku wykonywania kodu. Pliki w `~/.claude/instagram/` nie przetrwają między rozmowami, więc treść `voice.md` najlepiej wkleić do instrukcji projektu.

## Pierwszy krok: głos

Skopiujcie `templates/voice.md` do `~/.claude/instagram/voice.md` i uzupełnijcie pola `{{...}}`. Najszybciej: wklejcie trzy swoje rolki i napiszcie „uzupełnij voice.md na ich podstawie”. Każdy skill czyta ten plik.

## Trzynaście komend

| komenda | co robi |
| --- | --- |
| `/ig-reel` | Pomysł w rolkę: trzy hooki z oceną, scenariusz, napisy, rozpiska ujęć z czasami. |
| `/ig-viral` | Szuka rolek, które działają w niszy, ranking wg mnożnika ponad medianę konta, swipe file. |
| `/ig-caption` | Opis z podglądem tego, co widać przed „... więcej”, i linterem (w tym obietnice zdrowotne). |
| `/ig-carousel` | Karuzela: okładka, slajdy, slajd ze źródłami, pliki 1080x1350. |
| `/ig-story` | Relacje na dziś, naklejki, lejek do DM. |
| `/ig-profile` | Ocena profilu na 100 punktów i przepisanie bio. |
| `/ig-plan` | Plan tygodnia i lista kont do interakcji. |
| `/ig-human` | Humanizer: usuwa ślady AI, pięć testów. |
| `/ig-comment` | Komentarze pod cudzymi postami. Dziewięć typów, zero „🔥🔥🔥”. |
| `/ig-reply` | Odpowiedzi pod naszymi postami, z osobną ścieżką dla pytań medycznych. |
| `/ig-dm` | DM: słowo-klucz, pierwsza wiadomość, collab, dwa przypomnienia. |
| `/ig-repurpose` | Film z YouTube, live albo wykład w tydzień rolek i karuzel. |
| `/ig-audit` | Analiza opublikowanych postów: co działa i czego przestać. |

## Narzędzia (działają lokalnie, nic nie wysyłają)

```bash
python3 skills/ig-reel/hookscore.py hooki.txt           # ranking hooków
python3 skills/ig-reel/beats.py scenariusz.txt --target 30
python3 skills/ig-caption/caption.py opis.txt --keywords "insulinooporność"
python3 skills/ig-human/humanize.py szkic.txt --report
python3 skills/ig-human/detect.py szkic.txt czysty.txt
python3 skills/ig-viral/swipe.py zebrane.tsv --out ~/.claude/instagram/swipe.md
```

## Uczciwie o ograniczeniach

- **Ocena hooków nie przewiduje wyświetleń.** W oryginale dobrze odsiewała słabe hooki (AUC 0,83), a hity od wpadek tego samego twórcy prawie wcale (0,56, rzut monetą to 0,50). Wersja polska nie była testowana na polskim korpusie. Ostatnie słowo ma wykres utrzymania widzów.
- **Humanizer to heurystyki**, nie GPTZero ani inny detektor. Nie obiecuje „niewykrywalności”.
- **Liczby z Instagrama się starzeją.** Limit pięciu hashtagów obowiązuje od 18 grudnia 2025. Jeśli coś tu przeczy temu, jak Instagram działa dziś, rację ma Instagram.
- **Kontrola obietnic zdrowotnych łapie typowe frazy**, nie wszystko. Nie zastępuje przeczytania tekstu przez człowieka, a przy materiałach reklamowych i produktowych także sprawdzenia zgodności z przepisami.
- **Nic nie publikuje się samo.** Automatyczne publikowanie, komentowanie i masowe DM łamią regulamin Instagrama.

## Pliki

```
skills/ig-reel/hooks.json        26 polskich formuł hooków z regexami do rozpoznawania
skills/ig-reel/hookscore.py      pięć testów hooka + dyskwalifikacje
skills/ig-reel/beats.py          scenariusz -> rozpiska ujęć z czasami
skills/ig-caption/caption.py     podgląd feedu i linter opisu
skills/ig-human/slop.json        polski słownik: wypełniacze, frazy, wzorce, znaki
skills/ig-human/humanize.py      trzy przejścia czyszczące
skills/ig-human/detect.py        pięć testów „czy to AI”
skills/ig-viral/swipe.py         ranking wg mnożnika i rozpoznawanie formuł
skills/ig-profile/rubric.json    rubryka profilu na 100 punktów
templates/voice.md               profil głosu Braci Rodzeń
```

## Licencja

MIT. Oryginał: Jake Schincariol. Adaptacja PL: Bracia Rodzeń.
