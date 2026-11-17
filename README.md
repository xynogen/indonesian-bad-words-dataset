# Indonesian Bad Words Dataset

Daftar kata kasar bahasa Indonesia **plus pencocok** yang tahan leetspeak (`k0nt0l`), huruf ganda (`kontolll`) dan simbol sisipan (`kont*ol`).
Dataset ini belum lengkap; kontribusi kata baru diterima.

*Indonesian profanity list with a small matcher that handles leetspeak, repeated letters and inserted symbols.*

## Struktur

| Path | Isi |
|---|---|
| `data/words.csv` | Kata dasar (sudah dinormalkan): `word, category, ambiguous, source` |
| `badwords.py` | `normalize()`, `load()`, `find()` dan tes bawaan (`python badwords.py`) |

Varian seperti `4nj1ng`, `Anjinggg`, `ANJING` tidak disimpan satu per satu lagi. Semuanya dinormalkan ke `anjing`
(`4->a 3->e 1->i 0->o 5->s @->a !->i 9,6->g $->s 7->t`, huruf ganda jadi satu), jadi varian baru ikut tertangkap.

Kategori: `makian`, `seksual`, `hewan`, `bodoh`, `inggris`.
`ambiguous=1` berarti kata bisa biasa saja (`ayam`, `tahu`, `hitam`, `mati`, nama orang). Dilewati secara bawaan.

## Pakai

from badwords import find, load

find("dasar k0nt0l")            # ['kontol']
find("ayam goreng")             # []   (ayam = ambigu, dilewati)
find("ayam", load(include_ambiguous=True))      # ['ayam']
find("anjing", load({"seksual"}))               # []   (filter kategori)

Pencocokan per kata utuh, jadi `kontolan` tidak ditandai. Frasa (`anak lonte`) didukung. Angka murni (`1500`) aman.

## Batasan

- Tidak menangkap huruf yang dipisah spasi (`k o n t o l`) atau singkatan yang tidak ada di daftar.
- Leetspeak bisa salah tangkap di kata campur angka dan huruf (misal `b4`); kata ambigu dimatikan bawaan untuk mengurangi false positive.
- Kata baru ditambah dari pengetahuan umum, belum diuji pada teks nyata. Cek hasilnya sebelum dipakai untuk moderasi.

## Kontribusi

Tambah baris ke `data/words.csv` dalam bentuk **dinormalkan** (huruf kecil, tanpa angka, tanpa huruf ganda), lalu jalankan `python badwords.py`.

## License
[CC BY-NC](https://creativecommons.org/licenses/by-nc/4.0/legalcode)
