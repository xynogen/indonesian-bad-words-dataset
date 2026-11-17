# Indonesian Bad Words Dataset

Daftar kata kasar bahasa Indonesia (kata dasar) dan skrip untuk membuat file besar berisi variannya
(leetspeak `k0nt0l`, huruf ganda `kontolll`, huruf besar/kecil, simbol `anj!ng`). Dataset belum lengkap; kontribusi diterima.

*Indonesian profanity base-word list and a small CLI that generates a large variant file (CSV/JSON).*

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

## Sitasi

Lihat `CITATION.cff` (tombol *Cite this repository* di GitHub).

```bibtex
@software{Fikri_Indonesian_Bad_Words_Dataset_2026,
  author = {Fikri, Muhammad},
  month = {11},
  title = {{Indonesian Bad Words Dataset}},
  url = {https://github.com/xynogen/indonesian-bad-words-dataset},
  year = {2026}
}
```

## License
[MIT](LICENSE)
