# IF2150-2024-K01-G01-DetectiveTasksboard

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Supported OS](https://img.shields.io/badge/os-windows%20|%20macOS%20|%20linux-lightgrey)
![Flet](https://img.shields.io/badge/Flet-0.25.1-green?logo=flet&logoColor=white)
![FPDF](https://img.shields.io/badge/FPDF-1.7.2-orange?logo=fpdf&logoColor=white)
![Pylint](https://img.shields.io/badge/Pylint-3.3.2-yellow?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-7.4.0-red?logo=pytest&logoColor=white)


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

