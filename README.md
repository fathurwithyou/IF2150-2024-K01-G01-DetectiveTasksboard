# IF2150-2024-K01-G01-DetectiveTasksboard

# Badges for Project Requirements

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![OS](https://img.shields.io/badge/Supported%20OS-Windows%20|%20macOS%20|%20Linux-lightgrey?logo=windows)
![Flet](https://img.shields.io/badge/Flet-0.25.1-purple?logo=flet)
![FPDF](https://img.shields.io/badge/FPDF-1.7.2-orange?logo=readthedocs)
![Pandas](https://img.shields.io/badge/Pandas-1.5.3-teal?logo=pandas)
![Pillow](https://img.shields.io/badge/Pillow-10.1.0-green?logo=pillow)
![Pylint](https://img.shields.io/badge/Pylint-3.3.2-red?logo=pylint)
![Pytest](https://img.shields.io/badge/Pytest-7.4.0-yellow?logo=pytest)
![python-dateutil](https://img.shields.io/badge/python--dateutil-2.8.2-darkblue?logo=python)
![Typing](https://img.shields.io/badge/Typing-3.7.4.3-brown?logo=typeform)


![Detective Tasksboard Text Logo](image.png)

## Deskripsi Singkat

Detective Tasksboard adalah perangkat lunak yang dirancang untuk membantu lawyer dalam mengelola berbagai kasus hukum yang ditangani secara efisien dan terstruktur. Dengan perangkat lunak ini, pengelolaan data hukum menjadi lebih mudah, cepat, dan akurat.

## Instalasi Dependensi
Untuk menginstal perangkat lunak, ikuti langkah-langkah berikut:

1. Clone repository:
   ```bash
   git clone https://github.com/fathurwithyou/IF2150-2024-K01-G01-DetectiveTasksboard.git
   cd IF2150-2024-K01-G01-DetectiveTasksboard
   ```
2. Instalasi Dependensi: Pastikan Anda sudah menginstal Python. Kemudian jalankan perintah berikut:
   ```bash
   pip install -r requirements.txt
   ```
## Cara Menjalankan Program
Setelah semua dependensi terinstal dan directory berada di dalam IF2150-2024-K01-G01-DetectiveTasksboard, jalankan aplikasi dengan perintah:

1. Setelah semua dependensi terinstal, jalankan aplikasi dengan perintah:
   ```bash
   cd src
   python main.py
   ```
   
2. Aplikasi akan berjalan di antarmuka berbasis Flet dengan tampilan responsif dan real-time.

## Daftar Implementasi Modul

| Modul       | Penanggung Jawab             | Snapshot          |
|-------------|-------------------------------|-------------------|
| **Cases**   | Muhammad Fathur Rizky        | ![Cases](<img file>)  |
| **Victims** | Nathaniel Jonathan Rusli     | ![Victims](<img file>) |
| **Suspects**| Dave Daniel Yanni            | ![Suspects](<img file>)|
| **Detectives** | Alvin Christopher         | ![Detectives](<img file>)|
| **Dashboard** | Benedict Presley           | ![Dashboard](<img file>)|


## Daftar Tabel Basis Data

| Nama Tabel       | Atribut                                                                 |
|-------------------|-------------------------------------------------------------------------|
| **cases**         | id, judul, status, tanggal_mulai, tanggal_selesai, perkembangan_kasus, catatan |
| **detective_cases** | id_detective, id_kasus                                               |
| **detectives**    | id, nama, nik                                                         |
| **suspect_cases**  | id_suspect, id_kasus                                                 |
| **suspects**      | id, nama, foto, nik, usia, jk, catatan_kriminal                       |
| **victim_cases**   | id_victim, id_kasus                                                  |
| **victims**       | id, nama, foto, nik, usia, jk, hasil_forensik                         |

