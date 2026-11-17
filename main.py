"""Generate spelling variants (leetspeak, letter case, repeated last letter) of data/words.csv into CSV or JSON.

  python main.py -o out/variants.csv
  python main.py -o out/variants.json --case --repeat 2 --max 0
  python main.py --category hewan -o -
"""
import argparse
import csv
import itertools
import json
import os
import re
import sys

WORDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "words.csv")
DIGIT = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "g": "9", "t": "7"}
SYMBOL = {"a": "@", "i": "!", "s": "$"}  # only inside a word, never first or last
EXTRA = {"g": "6"}
LEET = str.maketrans("4310579@!$6", "aeiostgaisg")  # inverse of the three maps above


def deleet(text):
    """Inverse of the generator, minus the repeated-letter step: lower case, leetspeak back to letters."""
    return re.sub(r"[^a-z ]", "", text.lower().translate(LEET))


def variants(word, use_case, rep):
    """All leetspeak combinations of word (and of word with its last letter repeated up to rep extra times)."""
    out = set()
    for w in (word + word[-1] * k for k in range(rep + 1)):
        opts = []
        for i, ch in enumerate(w):
            edge = i in (0, len(w) - 1) or " " in w[i - 1:i + 2]
            subs = (DIGIT.get(ch), EXTRA.get(ch), None if edge else SYMBOL.get(ch))
            opts.append([ch] + [s for s in subs if s])
        out.update("".join(c) for c in itertools.product(*opts))
    if use_case:
        out |= {f(v) for v in out for f in (str.upper, str.title)}
    # Drop variants with no letter left ("tt" -> "77"), they would match plain numbers.
    out = [v for v in out if re.search("[a-z]", v, re.I)]
    return sorted(out, key=lambda v: (sum(a != b for a, b in zip(v.lower(), word)), len(v), v))


def test():
    assert "k0nt0ll" in variants("kontol", False, 2)
    assert "KONTOL" in variants("kontol", True, 0) and "Kontol" in variants("kontol", True, 0)
    assert all(v[0] not in "@!$" and v[-1] not in "@!$" for v in variants("anjing", False, 0))
    assert "b00bs" in variants("boobs", False, 0)        # real double letters stay
    assert "77" not in variants("tt", False, 0)              # no-letter variants dropped
    with open(WORDS, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len({r["word"] for r in rows}) == len(rows), "duplicate word"
    for r in rows:
        assert r["word"] == r["word"].strip().lower() and deleet(r["word"]) == r["word"], r
        assert r["ambiguous"] in ("0", "1") and r["source"] in ("survey", "ai"), r
        squash = re.sub(r"(.)\1+", r"\1", r["word"])
        for v in variants(r["word"], True, 2):              # every variant maps back to its word
            assert re.sub(r"(.)\1+", r"\1", deleet(v)) == squash, (v, r)
    print(f"test OK, {len(rows)} words")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-o", "--output", default="-", help="file keluaran (.csv/.json), '-' = stdout (csv)")
    p.add_argument("--category", action="append", help="batasi kategori, boleh diulang")
    p.add_argument("--all", action="store_true", help="ikutkan kata ambigu")
    p.add_argument("--case", action="store_true", help="tambah UPPER dan Title")
    p.add_argument("--repeat", type=int, default=0, metavar="N", help="ulang huruf terakhir sampai N kali tambahan")
    p.add_argument("--max", type=int, default=50, metavar="N", help="maks varian per kata, 0 = semua")
    p.add_argument("--test", action="store_true", help="jalankan cek bawaan")
    a = p.parse_args()
    if a.test:
        return test()

    with open(WORDS, encoding="utf-8", newline="") as f:
        words = [r for r in csv.DictReader(f)
                 if (a.all or r["ambiguous"] == "0") and (not a.category or r["category"] in a.category)]
    rows = [{"variant": v, "word": r["word"], "category": r["category"]}
            for r in words for v in variants(r["word"], a.case, a.repeat)[:a.max or None]]

    if a.output != "-":
        os.makedirs(os.path.dirname(a.output) or ".", exist_ok=True)
    with (sys.stdout if a.output == "-" else open(a.output, "w", encoding="utf-8", newline="")) as f:
        if a.output.endswith(".json"):
            json.dump(rows, f, ensure_ascii=False, indent=1)
            f.write("\n")
        else:
            w = csv.DictWriter(f, fieldnames=["variant", "word", "category"])
            w.writeheader()
            w.writerows(rows)
    print(f"{len(rows)} baris dari {len(words)} kata -> {a.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
