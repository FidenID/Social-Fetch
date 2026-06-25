# TokFetch

Downloader TikTok berbasis web — tinggal masukin URL, langsung ke download.

## Fitur

- Download video TikTok tanpa watermark
- Ekstrak audio MP3 (320kbps)
- Antarmuka web simpel, tinggal buka browser
- Auto-cleanup file setelah di-download
- Berjalan di local network (0.0.0.0)

## Persyaratan

- Python 3.10+
- ffmpeg (untuk konversi audio)
- yt-dlp (terinstall otomatis via pip)

## Instalasi

```bash
git clone https://github.com/username/tokfetch.git
cd tokfetch
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

Pastikan `ffmpeg` sudah terinstall di sistem:

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Arch
sudo pacman -S ffmpeg

# macOS
brew install ffmpeg
```

## Menjalankan

```bash
bash start.sh
```

Atau manual:

```bash
venv/bin/python app.py
```

Buka **http://127.0.0.1:5000** di browser.

## Cara Pakai

1. Tempel URL TikTok di kolom
2. Pilih mode **Video** atau **Audio**
3. Klik Download
4. File langsung ter-download otomatis

## Struktur

```
tokfetch/
├── app.py            # Aplikasi Flask utama
├── requirements.txt  # Dependensi Python
├── start.sh          # Script menjalankan aplikasi
├── templates/        # Template HTML
│   ├── index.html
│   └── result.html
├── static/           # File statis (CSS)
├── downloads/        # Folder file sementara
└── venv/             # Virtual environment
```

## Teknologi

- **Flask** — web framework
- **yt-dlp** — engine download video
- **ffmpeg** — konversi audio
