import yt_dlp

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "default_search": "ytsearch",
}

FFMPEG_OPTIONS = {
    "options": "-vn"
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)