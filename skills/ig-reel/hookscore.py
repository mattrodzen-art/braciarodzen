#!/usr/bin/env python3
"""
hookscore.py - ocena pierwszego zdania rolki (hooka) po polsku.

Pięć lokalnych heurystyk liczonych z samego tekstu: długość, którą da się
powiedzieć w mniej niż trzy sekundy, coś konkretnego (liczba, nazwa), stawka,
najważniejsze słowo na początku, i widz, do którego mówimy. Do tego lista
"dealbreakerów": powitanie, wstęp w stylu "w tym filmie", prośba o uwagę,
hashtag lub emoji w hooku, oraz obietnica wyleczenia albo gwarancja efektu
(w treściach zdrowotnych to ryzyko prawne i powód do odrzucenia przez Metę).

Czym to NIE jest: przewidywaczem wyświetleń. Wersja angielska, na której to
oparto, dobrze odróżniała słabe hooki od normalnych (AUC 0.83), a hity od
wpadek tego samego twórcy prawie wcale (AUC 0.56, rzut monetą to 0.50).
Wersja polska nie była jeszcze testowana na polskim korpusie. Używaj jej do
odsiewania oczywiście słabych hooków, a o reszcie niech decyduje wykres
utrzymania widzów.

Każdy test zwraca 0-100. Więcej znaczy lepiej.

Użycie
  python3 hookscore.py hooki.txt              # jeden hook w linii, ranking
  python3 hookscore.py --hook "Insulina rośnie po owsiance bardziej niż po jajkach."
  python3 hookscore.py hooki.txt --json
"""

import argparse
import json
import re
import statistics
import sys

UP = "A-ZĄĆĘŁŃÓŚŹŻ"
LO = "a-ząćęłńóśźż"
WORD_RE = re.compile(r"[\w$%'’-]+", re.UNICODE)
NUMBER_RE = re.compile(
    r"\d[\d\s.,]*\d|\d"
    r"(?:\s?(?:%|zł|pln|kg|g\b|mg|kcal|mmol|mg/dl|dni|dnia|tyg|tygodni|mies|lat|lata|"
    r"godz|h\b|min|sek|s\b|razy|x\b))?",
    re.IGNORECASE)
PROPER_RE = re.compile(rf"(?<![.!?]\s)(?<!^)\b[{UP}][{LO}]{{2,}}\b")
ACRONYM_RE = re.compile(r"\b(?:HbA1c|HOMA(?:-IR)?|LDL|HDL|BMI|TSH|PCOS|IO|LCHF|WHO|NFZ)\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Liczebniki mówione. "Pięć kilo" jest tak samo konkretne jak "5 kg".
# "Jeden" i "pierwszy" celowo pominięte: częściej są wypełniaczem niż liczbą.
NUM_EXACT = {"dwa", "dwie", "dwóch", "dwoma", "trzy", "trzech", "trzema", "cztery",
             "czterech", "sto", "stu", "pół", "zero", "dwukrotnie", "trzykrotnie"}
NUM_PREFIX = ("pięć", "pięci", "sześć", "sześci", "siedem", "siedmi", "osiem", "ośmi",
              "dziewięć", "dziewięci", "dziesięć", "dziesięci", "jedenaś", "dwanaś",
              "trzynaś", "czternaś", "piętnaś", "szesnaś", "dwadzieś", "trzydzieś",
              "czterdzieś", "pięćdziesi", "tysiąc", "tysiące", "tysięc", "milion",
              "miliard", "połow", "procent", "kilogram", "kilo", "złot", "kalori")
# Pojęcia, które w naszej niszy są konkretem, nie ogólnikiem.
CONCRETE_PREFIX = ("insulin", "glukoz", "cukr", "keton", "trójgliceryd", "cholesterol",
                   "metformin", "wątrob", "trzustk", "fruktoz", "owsiank", "jajk",
                   "chleb", "masł", "mięs", "ryż", "makaron", "sok", "glikemi")

# Słowa, które coś stawiają na szali.
STAKES_EXACT = {"nie", "nikt", "nic", "nigdy", "ale", "bez", "już", "tylko", "zamiast",
                "wcale", "nadal", "wciąż", "vs", "mit", "mity", "źle", "dopóki", "jednak",
                "niż", "bardziej", "mniej", "kontra", "versus"}
STAKES_PREFIX = ("błąd", "błęd", "strac", "trac", "koszt", "przesta", "zakaz", "gorsz",
                 "najgorsz", "kłam", "prawd", "sekret", "ukry", "ryzyk", "niebezpiecz",
                 "ostrzeg", "ostrzeż", "żału", "oszuk", "szkodz", "szkodl", "zabij",
                 "zabój", "cukrzyc", "zawał", "udar", "uzależ", "choro", "problem",
                 "pomył", "porażk", "zmarnow", "wyrzuc", "usun", "zastąp", "zastąpi",
                 "zapłac", "myli", "mylisz", "mylicie", "zaskak", "dlaczego", "naprawdę")

WEAK_OPENERS = [
    "cześć", "hej", "siema", "witam", "witajcie", "dzień dobry", "dzisiaj", "dziś",
    "w tym", "w dzisiejszym", "no więc", "no", "więc", "dobra", "okej", "ok",
    "słuchajcie", "słuchaj", "generalnie", "w sumie", "szczerze", "chciałbym",
    "chciałabym", "chcielibyśmy", "chcemy", "chciałem", "chciałam", "postanowiliśmy",
    "jest to", "to jest", "jak wiecie", "jak wiesz", "pewnie", "czy wiesz", "czy wiecie",
    "czy zastanawia", "jednym z", "jedną z", "jeśli chodzi o", "w dzisiejszych czasach",
    "mam dla", "mamy dla", "zapraszam", "zapraszamy", "porozmawiajmy", "dziś porozmawiamy",
]

IMPERATIVE_PREFIX = ("przesta", "skopiuj", "ukradnij", "usuń", "spróbuj", "zobacz",
                     "patrz", "zapisz", "zrób", "zacznij", "wyrzuć", "sprawdź", "odstaw",
                     "zjedz", "policz", "zmierz", "odpuść", "wyłącz", "napisz", "nie",
                     "nigdy", "pamiętaj", "posłuchaj", "rzuć", "zapomnij", "porównaj")

YOU_RE = re.compile(
    r"\b(?:ty|ci|cię|ciebie|tobie|twój|twoja|twoje|twojego|twojej|twoich|twoim|twoją|"
    r"wy|was|wam|wami|wasz|wasza|wasze|waszego|waszej|waszych|jesteś|jesteście)\b"
    r"|\b\w{2,}(?:esz|isz|ysz|asz|łeś|łaś)\b"
    r"|\b(?:jecie|macie|wiecie|robicie|myślicie|pijecie|jadacie|znacie|chcecie|"
    r"możecie|mówicie|liczycie|bierzecie|kupujecie)\b",
    re.IGNORECASE)
WE_RE = re.compile(
    r"\b(?:ja|mnie|mi|mój|moja|moje|my|nas|nam|nasz|nasza|nasze|naszego|naszych)\b"
    r"|\b\w{2,}(?:imy|ymy|emy|amy|łem|łam|liśmy|łyśmy)\b",
    re.IGNORECASE)

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:przestań scrollować|nie scrolluj|zatrzymaj się|stop[,!]? nie przewijaj)"),
     "Zaczyna się od prośby o uwagę. Hook ma na uwagę zasłużyć, nie o nią prosić."),
    (re.compile(r"(?i)\b(?:w (?:tym|dzisiejszym) (?:filmie|odcinku|poście|nagraniu|reelsie|rolce)|"
                r"pokażę (?:ci|wam)|pokażemy (?:ci|wam)|opowiem (?:ci|wam)|opowiemy (?:ci|wam))\b"),
     "Wstęp zapowiadający. Wytnij go i zacznij od konkretu."),
    (re.compile(r"(?i)^\s*(?:cześć|hej|siema|witam|witajcie|dzień dobry|elo)\b"),
     "Powitanie. Nikt nie przewija feedu, żeby się z kimś przywitać."),
    (HASHTAG_RE, "Hashtag w hooku. Hashtagi idą na dół opisu, jeśli w ogóle."),
    (EMOJI_RE, "Emoji w hooku. Tekst na ekranie ma miejsce na słowa albo na emoji, nie na oba."),
    (re.compile(r"(?i)\b(?:wyleczysz|wyleczycie|wyleczy (?:cię|was)|gwarantuj\w*|gwarancj\w* efekt\w*|"
                r"cudown\w*|100\s?% skuteczn\w*|na zawsze pozbędziesz|bez wysiłku schudniesz)"),
     "Obietnica wyleczenia lub gwarantowanego efektu. W treściach zdrowotnych to ryzyko "
     "prawne i powód blokady reklamy. Opisz mechanizm albo czyjś realny wynik zamiast obietnicy."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "18 000" i "18.000" mówi się jako jedno słowo liczbowe.
    return WORD_RE.findall(re.sub(r"(?<=\d)[\s.,](?=\d{3}\b)", "", text))


def low_words(text):
    return [w.lower().strip("'’-") for w in words(text)]


def is_num_word(w):
    return w in NUM_EXACT or w.startswith(NUM_PREFIX)


def is_stake(w):
    return w in STAKES_EXACT or (len(w) > 3 and w.startswith(STAKES_PREFIX))


def check_length(text, wps):
    n = len(words(text))
    secs = n / wps
    chars = len(text.strip())
    # Polskie słowa są dłuższe niż angielskie, więc okno jest przesunięte w dół.
    if 4 <= n <= 10:
        score = 100.0
    elif n < 4:
        score = clamp(100 - (4 - n) * 22)
    else:
        score = clamp(100 - (n - 10) * 12)
    if chars > 65:
        score -= 12
    return clamp(score), f"{n} słów, {chars} znaków, ~{secs:.1f}s mówione (cel: 4-10 słów)"


def check_specificity(text):
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text)) | set(ACRONYM_RE.findall(text))
    lw = low_words(text)
    spoken = [w for w in lw if is_num_word(w)]
    things = [w for w in lw if w.startswith(CONCRETE_PREFIX)]
    hits = len(nums) + len(propers) + len(spoken) + min(len(things), 1)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2] + things[:1])
    return score, (f"{hits} konkret(y)" + (f": {found}" if found else
                   " - żadnej liczby, nazwy ani rzeczy, którą da się sprawdzić"))


def check_stakes(text):
    markers = sorted({w for w in low_words(text) if is_stake(w)})
    if re.search(r"\d\s?zł|\bzłot", text, re.IGNORECASE):
        markers.append("cena")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    return clamp(score), (f"{n} znacznik(i) napięcia" + (f": {', '.join(markers[:4])}"
                          if markers else " - w tym zdaniu nic nie jest na szali"))


def check_frontload(text):
    w = words(text)
    if not w:
        return 0.0, "puste"
    lw = low_words(text)
    opener = " ".join(lw[:3])
    penalty, hit = 0, None
    for weak in WEAK_OPENERS:
        if opener == weak or opener.startswith(weak + " ") or lw[0] == weak:
            penalty, hit = 30, weak
            break
    payload = None
    for i, tok in enumerate(lw):
        if (is_stake(tok) or is_num_word(tok) or tok.startswith(CONCRETE_PREFIX)
                or NUMBER_RE.fullmatch(w[i]) or ACRONYM_RE.fullmatch(w[i])
                or (i and PROPER_RE.fullmatch(w[i]))):
            payload = i
            break
    if payload is None:
        base, where = 30.0, "w zdaniu nie ma słowa, które niesie treść"
    elif payload <= 2:
        base, where = 100.0, f"konkret na słowie {payload + 1}"
    elif payload <= 5:
        base, where = 70.0, f"konkret na słowie {payload + 1}, można przesunąć do przodu"
    else:
        base, where = 40.0, f"konkret dopiero na słowie {payload + 1}, za późno"
    return clamp(base - penalty), where + (f"; słabe otwarcie \"{hit}\"" if hit else "")


def check_address(text):
    lw = low_words(text)
    if YOU_RE.search(text):
        return 100.0, "mówi do widza"
    if lw and lw[0].startswith(IMPERATIVE_PREFIX):
        return 90.0, f"tryb rozkazujący na początku (\"{lw[0]}\")"
    if WE_RE.search(text):
        return 70.0, "pierwsza osoba (my/ja), widz nienazwany"
    return 35.0, "trzecia osoba, nikogo nie ma w pokoju"


CHECKS = ["DŁUGOŚĆ", "KONKRET", "STAWKA", "POCZĄTEK", "ADRESAT"]


def run(text, wpm=140):
    wps = wpm / 60.0
    results = {
        "DŁUGOŚĆ": check_length(text, wps),
        "KONKRET": check_specificity(text),
        "STAWKA": check_stakes(text),
        "POCZĄTEK": check_frontload(text),
        "ADRESAT": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    overall = clamp(statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15)
    verdict = "MOCNY" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "SŁABY")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nOCENA HOOKA", file=out)
    print("=" * 62, file=out)
    print(f"  „{text.strip()}”\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'WYNIK':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  DYSKWALIFIKACJA  {f}", file=out)
    if verdict != "MOCNY":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Najsłabsze: {weakest}. Popraw to i uruchom jeszcze raz.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING HOOKÓW\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        najsłabsze: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        dyskwalifikacja: {f}", file=out)
    print("\nNagrywajcie pierwszy. Jeśli pierwszy ma poniżej 50, żaden z tych nie jest hookiem.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Ocena hooka rolki w pięciu testach (PL).")
    ap.add_argument("input", nargs="?", default="-", help="plik z hookami (jeden w linii) albo -")
    ap.add_argument("--hook", help="oceń jeden hook podany w poleceniu")
    ap.add_argument("--wpm", type=float, default=140, help="tempo mówienia, słowa/min (domyślnie 140)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("brak tekstu do oceny", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line, args.wpm)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return
    if len(payload) == 1:
        render_one(lines[0], *run(lines[0], args.wpm))
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))
    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
