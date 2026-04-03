# SecurePass Manager

Aplikasi manajemen password desktop dengan generator otomatis dan penyimpanan lokal menggunakan SQLite.

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Fitur

- **Generator Password Otomatis** - Membuat password 12 karakter dengan kombinasi huruf besar, kecil, angka, dan simbol
- **Indikator Kekuatan Password** - Feedback real-time tentang keamanan password
- **Penyimpanan Lokal** - Database SQLite untuk menyimpan riwayat password
- **Export ke TXT** - Export riwayat password ke file teks
- **Dark Theme UI** - Antarmuka modern dengan tema gelap
- **Tanpa Internet** - Semua data tersimpan secara lokal di perangkat Anda

## Screenshot

```
┌─────────────────────────────────────────────────────────┐
│              SECUREPASS MANAGER                          │
│        Advanced Password Management & Generator          │
├─────────────────────────────────────────────────────────┤
│ Password: [xK9#mP2$vL7q    ] [Generate] [Copy]         │
│ Password belum mencapai 10 karakter (12 karakter)        │
├─────────────────────────────────────────────────────────┤
│ Nama/Keterangan: [Facebook Account        ] [Simpan]   │
├─────────────────────────────────────────────────────────┤
│  No  │ Nama/Keterangan    │ Password     │ Tanggal     │
├──────┼────────────────────┼──────────────┼─────────────┤
│  1   │ Facebook Account    │ xK9#mP2$vL7q │ 2026-04-04  │
│  2   │ Gmail               │ aB3$kL9#mN2p │ 2026-04-03  │
├─────────────────────────────────────────────────────────┤
│                              [Hapus Terpilih] [Export]  │
└─────────────────────────────────────────────────────────┘
```

## Instalasi

### Prasyarat
- Python 3.10+
- PyInstaller (untuk build executable)

### Menjalankan dari Source

```bash
# Clone repository
git clone https://github.com/Aapprzl/SecurePass-Manager.git
cd SecurePass-Manager

# Install dependensi (jika perlu)
pip install pyinstaller

# Jalankan aplikasi
python securepass.py
```

### Build ke Executable

```bash
pyinstaller SecurePass.spec --clean
```

Executable akan tersedia di folder `dist/SecurePass.exe`

## Penggunaan

1. **Generate Password** - Klik tombol "Generate Password" untuk membuat password baru
2. **Salin** - Klik "Copy" untuk menyalin password ke clipboard
3. **Simpan** - Masukkan nama/keterangan, lalu klik "Simpan"
4. **Hapus** - Pilih baris di tabel, klik "Hapus Terpilih"
5. **Export** - Klik "Print / Export TXT" untuk export riwayat ke file

## Struktur File

```
SecurePass Manager/
├── securepass.py        # Main application
├── securepass.db       # SQLite database (auto-generated)
├── icon.ico            # App icon
├── SecurePass.spec     # PyInstaller configuration
└── dist/               # Built executable
```

## Keamanan

- Password disimpan secara lokal, tidak dikirim ke server manapun
- Database SQLite dapat dienkripsi dengan tool pihak ketiga jika diperlukan
- Selalu backup file `securepass.db` secara berkala

## Lisensi

MIT License

## Kontribusi

Silakan buat issue atau pull request jika menemukan bug atau ingin menambahkan fitur.
