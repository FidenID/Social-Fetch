# TokFetch

Downloader video/audio dari berbagai sosial media — tinggal masukin URL, langsung ke download.

Didukung oleh **yt-dlp**: TikTok, Instagram, Facebook, YouTube, Twitter/X, Reddit, dan masih banyak lagi.

## Fitur

- Download video dari TikTok, Instagram Reels/Post, Facebook, YouTube, Twitter/X, dll
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
git clone https://github.com/FidenID/Downloader-Video-Tiktok.git
cd Downloader-Video-Tiktok
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

1. Copy link dari TikTok, Instagram, Facebook, YouTube, atau platform lainnya
2. Tempel link di kolom
3. Pilih mode **Video** atau **Audio**
4. Klik Download
5. File langsung ter-download otomatis

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
- **yt-dlp** — engine download video (support 1000+ situs)
- **ffmpeg** — konversi audio

## Deploy ke VPS

```bash
# Install
sudo apt install nginx certbot python3-certbot-nginx ffmpeg
pip install gunicorn

# Jalanin pake Gunicorn
gunicorn -w 2 -b 127.0.0.1:5000 app:app

# Reverse proxy Nginx + SSL
sudo certbot --nginx -d domainmu.com
```
