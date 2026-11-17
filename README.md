# Indonesian Bad Words Dataset

313 kata kasar bahasa Indonesia dari survei mahasiswa Politeknik Negeri Sriwijaya (2020), sudah dibersihkan,
dinormalkan, dan diberi kategori. `main.py` mengubahnya menjadi ribuan varian ejaan (`k0nt0l`, `kontolll`, `ANJ!NG`)
dalam CSV atau JSON, siap dipakai untuk filter kata, moderasi konten, atau data latih NLP.

*313 Indonesian profanity base words from a 2020 student survey, cleaned and categorized, plus a CLI that expands them
into thousands of spelling variants (CSV/JSON) for filtering, moderation, or NLP training.*

## Struktur

| Path | Isi |
|---|---|
| `data/words.csv` | Kata dasar yang sudah dinormalkan: `word, category, ambiguous, source` |
| `main.py` | CLI pembuat varian (hanya stdlib Python) |

Kategori: `makian`, `seksual`, `hewan`, `bodoh`, `inggris`.
`ambiguous=1` berarti kata bisa biasa saja (`ayam`, `tahu`, `hitam`, `mati`, nama orang). Dilewati kecuali pakai `--all`.

## Pakai

python main.py -o out/variants.csv                              # leetspeak, maks 50 varian per kata
python main.py -o out/variants.json --case --repeat 2 --max 0   # semua varian, plus huruf besar dan huruf ganda
python main.py --category hewan -o -                            # ke stdout
python main.py --test

| Opsi | Arti |
|---|---|
| `-o` | File keluaran, `.json` atau lainnya (CSV). `-` = stdout. Folder dibuat otomatis |
| `--category` | Batasi kategori, boleh diulang |
| `--all` | Ikutkan kata ambigu |
| `--case` | Tambah `UPPER` dan `Title` |
| `--repeat N` | Ulangi huruf terakhir sampai N kali tambahan |
| `--max N` | Maks varian per kata (default 50, `0` = semua) |

Kolom keluaran: `variant, word, category`. Hasil ada di `out/` (tidak masuk git).
Peta leetspeak: `a=4/@`, `e=3`, `i=1/!`, `o=0`, `s=5/$`, `g=9/6`, `t=7`. Simbol tidak dipakai di awal atau akhir kata.
Dengan `--case --repeat 2 --max 0` hasilnya sekitar 280 ribu baris, jadi pakai `--max` untuk membatasi.

## Kontribusi

Tambah baris ke `data/words.csv` dalam bentuk **dinormalkan** (huruf kecil, tanpa angka, tanpa huruf ganda), lalu jalankan `python main.py --test`.

## Asal data

Kata dasar berasal dari survei mahasiswa Politeknik Negeri Sriwijaya, awal 2020, lalu dibersihkan dan dinormalkan
(varian ejaan digabung jadi satu kata dasar). Kolom `source` di `data/words.csv`: `survey` (279 kata, dari survei) dan
`baru` (34 kata, ditambah belakangan dari pengetahuan umum).

## Catatan

Kata `baru` belum diuji pada teks nyata. Cek dulu sebelum dipakai untuk moderasi.

## Anotator

Rian Ramanda Putra ([@rianrahmanda](https://github.com/rianrahmanda))

## Sitasi

Lihat `CITATION.cff` (tombol *Cite this repository* di GitHub).

```bibtex
@software{Putra_Indonesian_Bad_Words_Dataset_2020,
  author = {Putra, Rian Ramanda and Fikri, Muhammad},
  title = {{Indonesian Bad Words Dataset}},
  url = {https://github.com/xynogen/indonesian-bad-words-dataset},
  year = {2020},
  note = {Data collected early 2020; cleaned and normalized in 2026}
}
```

## License
[MIT](LICENSE)
