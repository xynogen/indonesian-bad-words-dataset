"""Deteksi kata kasar Indonesia, tahan leetspeak (k0nt0l), huruf ganda (kontolll) dan sisipan simbol (kont*ol, k.o.n.t.o.l).

Pakai:  from badwords import find;  find("dasar k0nt0l")  ->  ["kontol"]
Cek:    python badwords.py     (jalankan tes bawaan)
"""
import csv
import re
from pathlib import Path

DATA = Path(__file__).parent / "data" / "words.csv"
LEET = str.maketrans("43105@!96$7", "aeiosaiggst")  # 4->a 3->e 1->i 0->o 5->s @->a !->i 9,6->g $->s 7->t


def normalize(text):
    """Huruf kecil, leetspeak jadi huruf, huruf ganda jadi satu. Token tanpa huruf (angka murni) dibiarkan."""
    out = []
    for tok in text.lower().split():
        tok = re.sub(r"^\W+|\W+$", "", tok)
        if not re.search(r"[a-z]", tok):
            if tok:
                out.append(tok)
            continue
        tok = re.sub(r"[*._\-]", "", tok).translate(LEET)
        tok = re.sub(r"(.)\1+", r"\1", re.sub(r"[^a-z]", "", tok))
        if tok:
            out.append(tok)
    return out


def load(categories=None, include_ambiguous=False):
    """Baca data/words.csv. Kata ambigu (nama makanan, hewan biasa, dsb.) dilewati kecuali diminta."""
    with open(DATA, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return {r["word"]: r["category"] for r in rows
            if (include_ambiguous or r["ambiguous"] == "0") and (not categories or r["category"] in categories)}


def find(text, words=None):
    """Kembalikan kata kasar (bentuk dasar) yang ada di teks. Cocok per kata utuh, bukan potongan kata."""
    words = words if words is not None else load()
    toks = normalize(text)
    longest = max((w.count(" ") + 1 for w in words), default=1)
    hits, i = [], 0
    while i < len(toks):
        for n in range(min(longest, len(toks) - i), 0, -1):
            cand = " ".join(toks[i:i + n])
            if cand in words:
                hits.append(cand)
                i += n
                break
        else:
            i += 1
    return hits


def _selftest():
    assert normalize("K0nt0lll!") == ["kontol"]
    assert find("dasar k0nt0l") == ["kontol"]
    assert find("Anjinggg lu, b4b1!") == ["anjing", "babi"]
    assert find("kont*ol") == ["kontol"]
    assert find("anak lonte") == ["anak lonte"]            # frasa
    assert find("kamu cantik sekali") == []
    assert find("ayam goreng dan tahu tempe") == []        # ambigu dilewati
    assert find("ayam", load(include_ambiguous=True)) == ["ayam"]
    assert find("kontolan") == []                          # bukan kata utuh, tidak ditandai
    assert find("harga 3 juta 1500 unit") == []            # angka murni aman
    assert find("") == []
    cats = set(load().values())
    assert cats == {"makian", "seksual", "hewan", "bodoh", "inggris"}, cats
    print("selftest OK,", len(load()), "kata aktif,", len(load(include_ambiguous=True)), "semua")


if __name__ == "__main__":
    _selftest()
