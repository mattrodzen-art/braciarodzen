#!/usr/bin/env python3
"""
detect.py - pięć testów, jak bardzo tekst wygląda na pisany przez maszynę (wersja polska).

What this is:  five local heuristics modelled on the signals public AI
detectors actually measure - sentence-length variation, concreteness, stock
vocabulary, typographic fingerprint, and voice. Every score is computed on
your machine from the text alone. Nothing is uploaded.

What this is NOT:  GPTZero, Originality, Copyleaks, Winston or Turnitin.
It does not call their APIs and it cannot promise their verdict. It catches
the things they all key on, which is why fixing them tends to move their
numbers too - but the only honest claim is the one on this line.

Each check returns a HUMAN score from 0 to 100. Higher is better.

Usage
  python3 detect.py draft.txt
  pbpaste | python3 detect.py -
  python3 detect.py draft.txt --json
  python3 detect.py before.txt after.txt      # compare two drafts
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
# Po polsku nie ma skrótów typu "don't". W ich miejsce: bezosobowość, którą
# AI lubi ("należy", "warto", "można zauważyć", "zostało"), kontra osoba.
IMPERSONAL = re.compile(r"(?i)\b(?:należy|warto|można zauważyć|można stwierdzić|jest to|"
                        r"stanowi|stanowią|zostało|zostały|został|dokonano|wskazuje się|"
                        r"uważa się|przyjmuje się|wydaje się)\b")
PRONOUNS = re.compile(
    r"(?i)\b(?:ja|mnie|mi|mój|moja|moje|my|nas|nam|nasz|nasza|nasze|naszych|ty|ci|cię|"
    r"ciebie|twój|twoja|twoje|wy|was|wam|wasz|wasza|wasze)\b"
    r"|\b\w{1,}(?:imy|ymy|emy|amy|esz|isz|ysz|asz|łem|łam|liśmy|łeś|łaś|cie)\b")
NUMBERS = re.compile(r"\b\d[\d\s,.]*%?|\d+\s?zł")
DOMAIN = re.compile(r"(?i)\b(?:HbA1c|HOMA|LDL|HDL|BMI|PCOS|insulin\w*|glukoz\w*|keton\w*|"
                    r"trójgliceryd\w*|cholesterol\w*|metformin\w*|fruktoz\w*)\b")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]{2,}\b", re.MULTILINE)


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Map value onto 0-100 where `human` -> 100 and `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text):
    """Humans vary sentence length hard. Models write even."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "za krótkie do oceny"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"zmienność {cv:.2f} w {len(lens)} zdaniach (cel 0.55+)"


def check_specificity(text):
    """Numbers, names and concrete nouns. Slop is abstract."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "za krótkie do oceny"
    per100 = 100 / len(w)
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text))) + len(set(m.lower()[:6] for m in DOMAIN.findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} konkretów, {density:.1f} na 100 słów (cel 4+)"


def check_slop(text, lex):
    """Stock vocabulary density against the lexicon."""
    w = words(text)
    if not w:
        return 50.0, "puste"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        pattern = re.compile(r"\b" + re.escape(entry["find"]).replace(r"\ ", r"\s+") + r"\b",
                             re.IGNORECASE)
        n = len(pattern.findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} wypełniaczy, {density:.1f} na 100 słów"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Characters a phone keyboard does not produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘“") + len(re.findall(r'"[^"\n]+"', text))
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} niewidocznych, {em} pauz (—), {curly} nie-polskich cudzysłowów, "
              f"{ellip} wielokropków, {nbsp} twardych spacji")
    return score, detail


def check_voice(text, lex):
    """Contractions, person, and the shapes models default to."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "za krótkie do oceny"
    per100 = 100 / len(w)
    impersonal = len(IMPERSONAL.findall(text)) * per100
    person = len(PRONOUNS.findall(text)) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(impersonal, human=0.0, machine=3.0) * 0.35
             + scale(person, human=8.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("uniform-bullets")
    detail = (f"{impersonal:.1f} form bezosobowych, {person:.1f} form osobowych "
              f"na 100 słów, {tells} wzorzec(ów)")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["RYTM", "KONKRET", "WYPEŁNIACZE", "ODCISK", "GŁOS"]


def run(text, lex):
    results = {}
    results["RYTM"] = check_burstiness(text)
    results["KONKRET"] = check_specificity(text)
    results["WYPEŁNIACZE"] = check_slop(text, lex)
    results["ODCISK"] = check_fingerprint(text)
    results["GŁOS"] = check_voice(text, lex)
    scores = [results[c][0] for c in CHECKS]
    # The weakest check drags the verdict: a detector only needs one signal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "OK" if overall >= 70 and min(scores) >= 55 else (
        "DO POPRAWY" if overall >= 50 else "WYGLĄDA NA AI")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANEL WYKRYWANIA AI" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'WYNIK LUDZKI':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "OK":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Najsłabszy sygnał: {weakest}. Napraw go najpierw.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Score how machine-written a draft looks.")
    ap.add_argument("input", nargs="?", default="-", help="file, or - for stdin")
    ap.add_argument("compare", nargs="?", help="second file, to show before/after")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "OK" else 1)


if __name__ == "__main__":
    main()
