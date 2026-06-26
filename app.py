import os
import subprocess
import uuid
import re
import zipfile
import io
from flask import Flask, render_template, request, Response

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

for f in os.listdir(DOWNLOAD_DIR):
    try:
        os.remove(os.path.join(DOWNLOAD_DIR, f))
    except Exception:
        pass

def sanitize_filename(name):
    return re.sub(r'[^\w\-_\. ]', '', name)

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        mode = request.form.get('mode', 'video')

        if not url:
            return render_template('index.html', error='Masukin URL dulu ya!')

        file_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_DIR, f'{file_id}_%(id)s.%(ext)s')

        venv_bin = os.path.join(BASE_DIR, 'venv', 'bin')
        yt_dlp_path = os.path.join(venv_bin, 'yt-dlp')

        if mode == 'photo':
            yt_cmd = [
                yt_dlp_path,
                '--no-playlist',
                '--no-warnings',
                '--ignore-errors',
                '-o', output_template,
                url,
            ]
        else:
            yt_cmd = [
                yt_dlp_path,
                '-f', 'bv[height<=1080]+ba/b[height<=1080]/best',
                '--merge-output-format', 'mp4',
                '--no-playlist',
                '--no-warnings',
                '-o', output_template,
                url,
            ]

        try:
            result = subprocess.run(yt_cmd, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                return render_template('index.html', error=f'Gagal download: {result.stderr[:500]}')

            downloaded_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(file_id)]
            if not downloaded_files:
                return render_template('index.html', error='File hasil download gak ketemu.')

            if mode == 'photo':
                image_files = sorted(
                    [f for f in downloaded_files if os.path.splitext(f)[1].lower() in IMAGE_EXTS]
                )
                if not image_files:
                    return render_template('index.html', error='Gak ada foto yang ditemukan di link itu.')

                if len(image_files) == 1:
                    target_file = os.path.join(DOWNLOAD_DIR, image_files[0])
                    ext = os.path.splitext(target_file)[1].lower()
                    mimetype_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.gif': 'image/gif', '.avif': 'image/avif'}
                    mimetype = mimetype_map.get(ext, 'image/jpeg')
                    download_name = image_files[0]

                    file_size = os.path.getsize(target_file)
                    headers = {
                        'Content-Disposition': f'attachment; filename="{download_name}"',
                        'Content-Length': str(file_size),
                    }

                    def stream_img():
                        try:
                            with open(target_file, 'rb') as f:
                                while chunk := f.read(65536):
                                    yield chunk
                        finally:
                            try:
                                os.remove(target_file)
                            except Exception:
                                pass

                    return Response(stream_img(), mimetype=mimetype, headers=headers)

                buf = io.BytesIO()
                with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for fn in image_files:
                        fp = os.path.join(DOWNLOAD_DIR, fn)
                        zf.write(fp, fn)
                        os.remove(fp)
                buf.seek(0)
                zip_data = buf.getvalue()

                for fn in downloaded_files:
                    if fn not in image_files:
                        try:
                            os.remove(os.path.join(DOWNLOAD_DIR, fn))
                        except Exception:
                            pass

                return Response(
                    zip_data,
                    mimetype='application/zip',
                    headers={
                        'Content-Disposition': f'attachment; filename="{file_id}_photos.zip"',
                        'Content-Length': str(len(zip_data)),
                    }
                )

            raw_file = os.path.join(DOWNLOAD_DIR, downloaded_files[0])
            base, ext = os.path.splitext(raw_file)
            download_name = downloaded_files[0]

            if mode == 'audio':
                audio_path = base + '.mp3'
                ff_cmd = [
                    'ffmpeg', '-i', raw_file,
                    '-vn', '-acodec', 'libmp3lame',
                    '-ab', '320k',
                    '-y', audio_path
                ]
                subprocess.run(ff_cmd, capture_output=True, text=True, timeout=300)
                os.remove(raw_file)
                target_file = audio_path
                download_name = os.path.basename(audio_path)
                mimetype = 'audio/mpeg'
            else:
                target_file = raw_file
                mimetype = 'video/mp4'

            if not os.path.exists(target_file):
                return render_template('index.html', error='File hasil gak ditemukan.')

            file_size = os.path.getsize(target_file)

            def stream_and_cleanup():
                try:
                    with open(target_file, 'rb') as f:
                        while chunk := f.read(65536):
                            yield chunk
                finally:
                    try:
                        os.remove(target_file)
                    except Exception:
                        pass

            headers = {
                'Content-Disposition': f'attachment; filename="{download_name}"',
                'Content-Length': str(file_size),
            }

            return Response(stream_and_cleanup(), mimetype=mimetype, headers=headers)

        except subprocess.TimeoutExpired:
            return render_template('index.html', error='Download timeout, coba lagi nanti.')
        except Exception as e:
            return render_template('index.html', error=f'Error: {str(e)[:300]}')

    return render_template('index.html')

if __name__ == '__main__':
    print('TokFetch jalan di http://127.0.0.1:5000')
    app.run(debug=False, host='0.0.0.0', port=5000)
