# Video Downloader App

A simple Flask-based web application that allows users to download videos or audio from various online sources. The app provides different formats for download and shows the download progress in real-time.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features
- **URL-based Video Download:** Enter a video URL to get download options.
- **Format Selection:** Choose from various available formats for audio and video.
- **Progress Tracking:** Real-time download progress bar.
- **Responsive Design:** Mobile-friendly UI built with Tailwind CSS.
- **Socket.IO Integration:** Real-time communication between server and client.

## Requirements
- Python 3.7+
- Flask
- Flask-SocketIO
- youtube-dl (or yt-dlp as an alternative)
- Gunicorn (for production)
- Socket.IO JavaScript client library

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/video-downloader-app.git
    cd video-downloader-app
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Install youtube-dl or yt-dlp:**
    ```bash
    pip install youtube-dl
    ```
    or
    ```bash
    pip install yt-dlp
    ```

5. **Run the Flask application:**
    ```bash
    flask run
    ```

    By default, the app will run on `http://127.0.0.1:5000`.

## Usage

1. **Access the app:**
   Open a web browser and navigate to `http://127.0.0.1:5000`.

2. **Download a video:**
   - Enter the URL of the video you want to download.
   - Select the desired format from the list of available options.
   - The download will begin, and the progress will be shown in real-time.

3. **Download Progress:**
   - The progress bar will indicate the percentage of the download completed.
   - Once the download is complete, the file will be available for download.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
