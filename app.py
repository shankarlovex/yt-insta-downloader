from flask import Flask, request, jsonify, send_file
import os, uuid, yt_dlp

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"message": "YT & INSTA Downloader Backend Running ✅"})

@app.route('/download/youtube', methods=['POST'])
def download_youtube():
    data = request.get_json()
    url = data.get("url")
    format_ = data.get("format", "mp4")
    quality = data.get("quality", "best")
    if not url:
        return jsonify({"error": "URL is required"}), 400
    try:
        filename = f"{uuid.uuid4()}.{format_}"
        output_path = os.path.join(DOWNLOAD_DIR, filename)
        ydl_opts = {
            'format': f'{quality}[ext={format_}]' if quality != 'best' else f'bestvideo+bestaudio/best',
            'outtmpl': output_path,
            'merge_output_format': format_,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/insta', methods=['POST'])
def download_instagram():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400
    try:
        filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(DOWNLOAD_DIR, filename)
        ydl_opts = {'outtmpl': output_path, 'quiet': True, 'merge_output_format': 'mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

