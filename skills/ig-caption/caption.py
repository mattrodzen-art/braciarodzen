#!/usr/bin/env python3
"""
caption.py - sprawdza opis na Instagram i pokazuje dokładnie to, co widać w feedzie
przed „... więcej”.

Feed pokazuje około 125 znaków opisu, resztę chowa za tapnięciem. Prawie każdy
opis, który nie działa, przegrywa właśnie tam. Skrypt rysuje to okno jako ramkę,
a potem sprawdza dziesięć rzeczy, w tym jedną dodaną dla treści zdrowotnych:
obietnice wyleczenia i gwarancje efektu.

125 znaków to przybliżenie. Prawdziwa granica zależy od telefonu i łamania linii,
dlatego warto mieć zapas. Zmienisz ją przez --truncate.

Użycie
  python3 caption.py opis.txt
  python3 caption.py opis.txt --keywords "insulinooporność,dieta niskowęglowodanowa"
  python3 caption.py opis.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200
TRUNCATE = 125
HASHTAG_LIMIT = 5        # Limit Instagrama od 18 grudnia 2025 (wcześniej 30).

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)", re.UNICODE)
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)", re.UNICODE)
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[\w-]+\.(?:pl|com|eu|io|net|org|ai|app)(?:/\S*)?\b",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(
    r"\d+|(?<![.!?]\s)(?<!^)\b[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]{2,}\b|"
    r"\b(?:HbA1c|HOMA|LDL|HDL|BMI|PCOS)\b|(?i:\b(?:insulin|glukoz|cukr|keton|trójgliceryd)\w*)",
    re.MULTILINE)

ASKS = [
    (re.compile(r"(?i)\b(?:napisz|wpisz|zostaw|dajcie|napiszcie|wpiszcie)\b[^.!?\n]{0,25}\bkomentarz\w*[^.!?\n]{0,20}\b[A-ZĄĆĘŁŃÓŚŹŻ0-9]{3,}\b"
                r"|\bskomentuj\w*\s+[„\"]?[A-ZĄĆĘŁŃÓŚŹŻ0-9]{3,}\b"), "słowo-klucz w komentarzu"),
    (re.compile(r"(?i)\b(?:napisz|napiszcie) do (?:nas|mnie)\b|\bwiadomoś\w+ prywatn\w*|\bna priv\b|\bw dm\b"), "napisz do nas"),
    (re.compile(r"(?i)\bzapisz(?:cie)? (?:ten post|to|sobie|tę|tą|ten)\b"), "zapisz"),
    (re.compile(r"(?i)\b(?:udostępnij\w*|wyślij(?:cie)? (?:to|ten)|podeślij\w*)\b"), "udostępnij"),
    (re.compile(r"(?i)\bobserwuj\w*\b"), "obserwuj"),
    (re.compile(r"(?i)\blink w bio\b|\blink (?:jest )?w profilu\b"), "link w bio"),
    (re.compile(r"(?i)\b(?:przesuń|przewiń|przesuńcie)\w*\b"), "przesuń"),
    (re.compile(r"(?i)\b(?:a (?:jak )?u (?:ciebie|was)|a ty\?|a wy\?|dajcie znać|który\w* (?:wybier|jest)|jak (?:to )?wygląda u)"), "pytanie do widza"),
]

FILLER_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#foryou", "#foryoupage",
               "#trending", "#instagood", "#love", "#follow", "#like4like", "#reels",
               "#reelsinstagram", "#viralreels", "#instadaily", "#dlaciebie", "#polska",
               "#instapolska", "#zdrowie", "#motywacja", "#fit"}

PROMISES = re.compile(
    r"(?i)\b(?:wyleczysz|wyleczycie|wyleczy (?:cię|was)|gwarantuj\w*|gwarancj\w*|cudown\w*|"
    r"100\s?% skuteczn\w*|na zawsze pozbędzi\w*|bez wysiłku|detoks\w*|oczyszcz\w* organizm\w*|"
    r"odstaw(?:cie)? (?:leki|metformin\w*|insulin\w*))")
VAGUE_AUTHORITY = re.compile(
    r"(?i)\b(?:badania (?:pokazują|dowodzą|wykazują|potwierdzają)|naukowcy (?:odkryli|twierdzą|udowodnili)|"
    r"eksperci (?:twierdzą|mówią|zalecają)|udowodniono naukowo|nauka (?:mówi|dowodzi))\b")


def visible_window(text, cut):
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  TO WIDAĆ W FEEDZIE", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... więcej" if truncated else "(cały opis się mieści)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    stripped = text.strip()
    chars = len(stripped)
    first_line = stripped.split("\n")[0].strip() if stripped else ""
    tags = HASHTAG_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    asks = [name for p, name in ASKS if p.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]
    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("DŁUGOŚĆ", "FAIL" if chars > LIMIT else "PASS",
        f"{chars} / {LIMIT} znaków" + (f", {chars - LIMIT} za dużo" if chars > LIMIT else ""))

    if not first_line:
        add("PIERWSZA LINIA", "FAIL", "opis zaczyna się od pustej linii")
    elif first_line[0] in "#@":
        add("PIERWSZA LINIA", "FAIL", "zaczyna się od hashtagu lub oznaczenia, a to jedyne miejsce warte zdania")
    elif EMOJI_RE.match(first_line):
        add("PIERWSZA LINIA", "WARN", "zaczyna się od emoji")
    elif len(first_line) > cut:
        add("PIERWSZA LINIA", "WARN", f"{len(first_line)} znaków, więc tnie się na {cut} w pół myśli. "
            "OK, jeśli cięcie jest cliffhangerem, źle, jeśli wypada w zdaniu podrzędnym")
    else:
        add("PIERWSZA LINIA", "PASS", f"{len(first_line)} znaków, mieści się w całości")

    n_conc = len(CONCRETE_RE.findall(window))
    add("KONKRET NA START", "PASS" if n_conc else "WARN",
        f"{n_conc} liczb(y)/nazw(y) w widocznym oknie" + ("" if n_conc else " - nic sprawdzalnego przed tapnięciem"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGI", "FAIL", f"{len(tags)} tagów, limit Instagrama to {HASHTAG_LIMIT}")
    elif filler:
        add("HASHTAGI", "WARN", f"{len(tags)} tagów, {len(filler)} ogólnych ({', '.join(filler[:3])}). Nic nie opisują")
    else:
        add("HASHTAGI", "PASS", f"{len(tags)} tag(ów)" + (f": {' '.join(tags)}" if tags else ""))

    if tags and any(t in window for t in tags):
        add("MIEJSCE TAGÓW", "WARN", "hashtag w widocznym oknie zabiera miejsce na treść")
    else:
        add("MIEJSCE TAGÓW", "PASS", "tagi pod zgięciem" if tags else "brak tagów")

    add("LINKI", "WARN" if links else "PASS",
        f"{len(links)} link(ów) w opisie, a linki w opisie nie są klikalne. Bio, stories albo DM"
        if links else "brak martwych linków")

    if len(asks) == 1:
        add("JEDNA PROŚBA", "PASS", f"jedno wezwanie: {asks[0]}")
    elif not asks:
        add("JEDNA PROŚBA", "WARN", "brak wezwania do działania. Zdecydujcie, po co jest ten post")
    else:
        add("JEDNA PROŚBA", "WARN", f"{len(asks)} prośby ({', '.join(asks)}). Dwie prośby to jak żadna")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "WARN" if density > 1.5 else "PASS",
        f"{len(emoji)} emoji, {density:.1f} na 100 znaków" + (" - za dużo jak na nasz styl" if density > 1.5 else ""))

    prom = sorted({m.group(0).lower() for m in PROMISES.finditer(stripped)})
    vague = sorted({m.group(0).lower() for m in VAGUE_AUTHORITY.finditer(stripped)})
    if prom:
        add("ZDROWIE: OBIETNICE", "FAIL", f"obietnica efektu lub ryzykowna porada: {', '.join(prom[:3])}. "
            "Opiszcie mechanizm albo realny przypadek, nie gwarantujcie wyniku")
    else:
        add("ZDROWIE: OBIETNICE", "PASS", "brak obietnic wyleczenia i gwarancji")
    if vague:
        add("ZDROWIE: ŹRÓDŁA", "WARN", f"„{vague[0]}” bez wskazania którego badania. "
            "Podajcie autora i rok albo przeformułujcie")

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        status = "PASS" if not missing else ("WARN" if found else "FAIL")
        add("FRAZY WYSZUKIWANIA", status, f"{len(found)}/{len(keywords)} obecnych"
            + (f". Brakuje: {', '.join(missing)}" if missing else "")
            + " (uwaga na odmianę: „insulinooporności” nie zawiera „insulinooporność”)")

    fails = sum(c["status"] == "FAIL" for c in checks)
    warns = sum(c["status"] == "WARN" for c in checks)
    verdict = "POPRAW" if fails else ("PRZEJRZYJ" if warns else "GOTOWE")
    return {"characters": chars, "visible": window, "truncated": chars > cut,
            "hashtags": tags, "links": links, "emoji": len(emoji), "asks": asks,
            "checks": checks, "verdict": verdict}


def render(a, out=sys.stdout):
    head = (f"KONTROLA OPISU  ·  {a['characters']} / {LIMIT} znaków  ·  "
            f"{len(a['hashtags'])} hashtagów  ·  {len(a['asks'])} prośb(a)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<5} {c['check']:<20} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  WERDYKT  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Kontrola opisu na Instagram (PL).")
    ap.add_argument("input", nargs="?", default="-")
    ap.add_argument("--truncate", type=int, default=TRUNCATE)
    ap.add_argument("--keywords", default="", help="frazy, po których chcecie być znajdowani, po przecinku")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    print(json.dumps(a, indent=2, ensure_ascii=False)) if args.json else render(a)
    sys.exit(0 if a["verdict"] == "GOTOWE" else 1)


if __name__ == "__main__":
    main()
