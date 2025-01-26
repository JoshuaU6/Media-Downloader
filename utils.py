import math
import os
from pathlib import Path


def get_download_dir():
    if os.name == "nt":  # Windows
        download_dir = Path(os.getenv("USERPROFILE")) / "Downloads"
    else:  # macOS and Linux
        download_dir = Path.home() / "Downloads"
    return download_dir


def format_size(size_bytes):
    # Convert bytes to a human-readable format (e.g., MB, GB)
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def format_duration(duration_seconds):
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = duration_seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes}:{seconds:02}"
