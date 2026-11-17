"""Buat permutasi (leetspeak, huruf besar/kecil, huruf ganda) dari kata dasar di data/words.csv, simpan ke CSV atau JSON.

  python main.py -o out/variants.csv                  # leetspeak, maks 50 varian per kata
  python main.py -o out/variants.json --case --repeat 2 --max 0
  python main.py --category hewan --all -o -          # '-' = stdout, format dari --format
  python main.py --test
"""
import argparse
import csv
import itertools
import json
import os
import sys

from badwords import load, normalize

# Kebalikan LEET di badwords.py. Simbol (@ ! $) hanya di tengah kata: normalize() membuang simbol di tepi token.
DIGIT = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "g": "9", "t": "7"}
SYMBOL = {"a": "@", "i": "!", "s": "$"}
EXTRA = {"g": "6"}


def leet(word):
    """Semua kombinasi substitusi huruf, yang paling sedikit diubah dulu."""
    opts = []
    for i, ch in enumerate(word):
        edge = i in (0, len(word) - 1) or " " in word[i - 1:i + 2]
        subs = [DIGIT.get(ch), EXTRA.get(ch), None if edge else SYMBOL.get(ch)]
        opts.append([ch] + [s for s in subs if s])
    combos = ("".join(c) for c in itertools.product(*opts))
    return sorted(combos, key=lambda v: (sum(a != b for a, b in zip(v, word)), v))


def repeat(word, n):
    """Huruf terakhir diulang sampai n kali: kontol, kontoll, kontolll."""
    return [word + word[-1] * k for k in range(n)]


def variants(word, use_case=False, rep=0):
    out = {word}
    if rep:
        out = {v for w in out for v in repeat(w, rep + 1)}
    out = {v for w in out for v in leet(w)}
    if use_case:
        out |= {f(v) for v in out for f in (str.upper, str.title)}
    # Buang yang tidak kembali ke kata dasar (misal 't' -> '7' jadi angka murni).
    return [v for v in sorted(out, key=lambda v: (len(v), v)) if normalize(v) == word.split()]


def generate(rows, use_case, rep, cap):
    for word, cat in rows:
        vs = variants(word, use_case, rep)
        for v in (vs[:cap] if cap else vs):
            yield {"variant": v, "word": word, "category": cat}


def write(rows, fmt, fh):
    rows = list(rows)
    if fmt == "json":
        json.dump(rows, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    else:
        w = csv.DictWriter(fh, fieldnames=["variant", "word", "category"])
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def test():
    assert normalize("k0nt0ll") == ["kontol"]
    assert "k0nt0l" in variants("kontol") and "k0nt0ll" in variants("kontol", rep=2)
    assert "anj!ng" in variants("anjing") and all(not v.startswith("!") for v in variants("anjing"))
    assert "KONTOL" in variants("kontol", use_case=True)
    assert "an@k l0nt3" in variants("anak lonte") or "4n@k l0nt3" in variants("anak lonte")
    assert variants("t") == ["t"]                     # '7' dibuang, bukan kembali ke 't'
    for word, _ in [(w, c) for w, c in load(include_ambiguous=True).items()][:80]:
        for v in variants(word, use_case=True, rep=2):
            assert normalize(v) == word.split(), (v, word)
    print("main.py test OK")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-o", "--output", default="-", help="file keluaran (.csv/.json), '-' = stdout")
    p.add_argument("--format", choices=["csv", "json"], help="paksa format (default dari ekstensi, lalu csv)")
    p.add_argument("--category", action="append", help="batasi kategori, boleh diulang")
    p.add_argument("--all", action="store_true", help="ikutkan kata ambigu")
    p.add_argument("--case", action="store_true", help="tambah UPPER dan Title")
    p.add_argument("--repeat", type=int, default=0, metavar="N", help="ulang huruf terakhir sampai N kali tambahan")
    p.add_argument("--max", type=int, default=50, metavar="N", help="maks varian per kata, 0 = semua")
    p.add_argument("--test", action="store_true")
    a = p.parse_args()
    if a.test:
        return test()
    fmt = a.format or ("json" if a.output.endswith(".json") else "csv")
    rows = load(a.category, a.all).items()
    if a.output != "-":
        os.makedirs(os.path.dirname(a.output) or ".", exist_ok=True)
    out = sys.stdout if a.output == "-" else open(a.output, "w", encoding="utf-8", newline="")
    with out:
        n = write(generate(rows, a.case, a.repeat, a.max), fmt, out)
    print(f"{n} baris dari {len(rows)} kata -> {a.output} ({fmt})", file=sys.stderr)


if __name__ == "__main__":
    main()
