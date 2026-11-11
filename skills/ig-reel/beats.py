#!/usr/bin/env python3
"""
beats.py - zamienia scenariusz rolki w rozpiskę ujęć z czasami, zanim nagracie.

Liczy, ile trwa wypowiedzenie każdej linii, układa je na osi czasu i flaguje
cztery rzeczy, które zabijają rolkę w montażu: hook dłuższy niż trzy sekundy,
ujęcie na tyle długie, że widz zdąży wyjść, kilka linii z rzędu bez żadnego
konkretu, oraz brak pętli (ostatnie zdanie nie wraca do pierwszego).

Czasy to szacunek ze słów na minutę. Polskie słowa są dłuższe niż angielskie,
więc domyślnie 140 słów/min. Zmierzcie swoje tempo raz (przeczytajcie na głos
scenariusz ze stoperem) i podawajcie je przez --wpm albo wpiszcie do voice.md.

Użycie
  python3 beats.py scenariusz.txt
  python3 beats.py scenariusz.txt --target 30
  python3 beats.py scenariusz.txt --wpm 150 --target 45
  python3 beats.py scenariusz.txt --json
"""

import argparse
import json
import re
import sys

WORD_RE = re.compile(r"[\w$%'’-]+", re.UNICODE)
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(
    r"\d+|(?<![.!?]\s)(?<!^)\b[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]{2,}\b|"
    r"\b(?:HbA1c|HOMA|LDL|HDL|BMI|TSH|PCOS)\b|"
    r"(?i:\b(?:insulin|glukoz|cukr|keton|trójgliceryd|cholesterol|kalori|kilogram|złot|procent)\w*)",
    re.MULTILINE)
STOPWORDS = {
    "i", "a", "w", "z", "na", "do", "o", "że", "to", "jest", "się", "nie", "ale", "czy",
    "jak", "co", "ten", "ta", "te", "tak", "po", "od", "za", "przez", "dla", "ty", "ci",
    "my", "nas", "nam", "wy", "was", "ja", "mi", "mnie", "jego", "jej", "ich", "był",
    "była", "było", "są", "być", "już", "tylko", "też", "więc", "bo", "gdy", "kiedy",
}

HOOK_WINDOW = 3.0
MAX_BEAT = 4.0
ABSTRACT_RUN = 3


def words(text):
    return WORD_RE.findall(re.sub(r"(?<=\d)[\s.,](?=\d{3}\b)", "", text))


def stem(w):
    """Polska odmiana: „insulina”, „insuliny”, „insulinę” to to samo słowo w pętli."""
    w = w.lower()
    return w[:5] if len(w) >= 5 else w


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def split_beats(raw, wps):
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            cand = (buf + " " + part).strip()
            if buf and len(words(cand)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = cand
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=140, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None
    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({"n": i + 1, "start": round(clock, 2), "dur": round(dur, 2), "words": n,
                     "text": text, "concrete": len(CONCRETE_RE.findall(text)),
                     "label": "", "flags": []})
        clock += dur
    total = clock

    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "HOOK"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "HOOK" else "HOOK/CTA"
    for r in rows:
        if not r["label"] and r["start"] <= total / 2 < r["start"] + r["dur"]:
            r["label"] = "ŚRODEK"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"hook trwa {rows[0]['dur']:.1f}s, dłużej niż {HOOK_WINDOW:.0f}s")
        notes.append(f"Ujęcie 1 trwa {rows[0]['dur']:.1f}s. Skróćcie do najwyżej "
                     f"{int(HOOK_WINDOW * wps)} słów, inaczej hook pada, gdy decyzja już zapadła.")
    if rows[0]["concrete"] == 0:
        notes.append("W ujęciu 1 nie ma liczby, nazwy ani konkretnej rzeczy. "
                     "Takie hooki się przewija.")
    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f}s na jednym ujęciu")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Ujęcia {', '.join(map(str, long_beats))} trwają ponad {MAX_BEAT:.0f}s. "
                     "Podzielcie linię albo zmieńcie obraz w jej trakcie. Statyczny kadr to "
                     "moment, w którym ludzie wychodzą.")
    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Ujęcia {start}-{r['n']} nie mają żadnego konkretu. "
                             "Wstawcie w jedno z nich liczbę, nazwę albo produkt.")
        else:
            run, start = 0, None

    first = {stem(w) for w in words(rows[0]["text"]) if w.lower() not in STOPWORDS}
    last = {stem(w) for w in words(rows[-1]["text"]) if w.lower() not in STOPWORDS}
    loop = sorted(first & last)
    if loop:
        notes.append(f"Pętla: ostatnie ujęcie wraca do „{', '.join(loop[:3])}…” z hooka. "
                     "Drugie obejrzenie to darmowy zasięg.")
    else:
        notes.append("Brak pętli. Ostatnie ujęcie nie ma wspólnego słowa z hookiem, więc film "
                     "kończy się płasko. Powtórzenie jednego słowa z ujęcia 1 to najtańszy replay.")
    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"Długość w punkt ({total:.1f}s przy celu {target:.0f}s).")
        elif delta > 0:
            notes.append(f"{delta:.1f}s ponad cel. Wytnijcie około {int(delta * wps)} słów.")
        else:
            notes.append(f"{-delta:.1f}s poniżej celu. Dodajcie ~{int(-delta * wps)} słów "
                         "albo nagrajcie krócej. Krócej zwykle jest lepiej.")
    return {"wpm": wpm, "target": target, "total_seconds": round(total, 2),
            "total_words": sum(r["words"] for r in rows), "beats": rows, "notes": notes}


def render(a, out=sys.stdout):
    head = (f"ROZPISKA UJĘĆ  ·  {a['total_words']} słów  ·  ~{a['total_seconds']:.1f}s "
            f"przy {a['wpm']:.0f} sł/min" + (f"  ·  cel {a['target']:.0f}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<9}" if r["label"] else " " * 9
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<9}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Rozpiska ujęć rolki z czasami (PL).")
    ap.add_argument("input", nargs="?", default="-")
    ap.add_argument("--wpm", type=float, default=140, help="tempo mówienia (domyślnie 140)")
    ap.add_argument("--target", type=float, help="docelowa długość w sekundach")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("pusty scenariusz", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(a, indent=2, ensure_ascii=False)) if args.json else render(a)


if __name__ == "__main__":
    main()
