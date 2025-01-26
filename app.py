import eventlet

eventlet.monkey_patch()

from flask import (
    Flask,
    request,
    render_template,
    jsonify,
    url_for,
    send_file,
    after_this_request,
)
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from utils import format_duration, format_size, get_download_dir
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/formats", methods=["POST"])
def get_formats():
    data = request.get_json()
    url = data["url"]
    ydl_opts = {}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get("formats", [])
        title = info_dict.get("title", "")
        thumbnail = info_dict.get("thumbnail", "")
        duration = info_dict.get("duration", 0)  # Duration in seconds

    # Update formats to include human-readable size and format duration
    for format in formats:
        format["filesize_human"] = format_size(format.get("filesize", 0))
        format["duration_human"] = format_duration(duration)

    return jsonify(
        {
            "url": url,
            "formats": formats,
            "title": title,
            "thumbnail": thumbnail,
            "duration": format_duration(duration),  # Include the formatted duration
        }
    )


def progress_hook(d):
    # Ensure this print statement is reached
    print(f"Progress: {d}")

    # Emit progress data to the client
    socketio.emit("progress", d)


@socketio.on("download")
def handle_download(data):
    url = data["url"]
    format_id = data["format_id"]
    download_type = data["type"]
    download_dir = get_download_dir()

    if download_type == "audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": str(download_dir / "%(title)s.%(ext)s"),
            "progress_hooks": [progress_hook],
        }
    else:
        ydl_opts = {
            "format": f"{format_id}+bestaudio/best",
            "outtmpl": str(download_dir / "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "progress_hooks": [progress_hook],
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url)
        filename = ydl.prepare_filename(result)

    emit(
        "download_complete",
        {"download_url": url_for("download_file", filename=os.path.basename(filename))},
    )


@app.route("/download_file/<filename>")
def download_file(filename):
    download_dir = get_download_dir()

    @after_this_request
    def remove_file(response):
        try:
            os.remove(download_dir / filename)
        except Exception as e:
            app.logger.error("Error removing or closing downloaded file handle", e)
        return response

    return send_file(download_dir / filename, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, debug=False, host="0.0.0.0", port=port, server=eventlet)