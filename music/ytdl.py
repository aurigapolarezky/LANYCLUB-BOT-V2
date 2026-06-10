import yt_dlp
import asyncio

async def get_song_info(query: str):
    loop = asyncio.get_event_loop()

    data = await loop.run_in_executor(
        None,
        lambda: ytdl.extract_info(
            query,
            download=False
        )
    )

    if "entries" in data:
        data = data["entries"][0]

    return {
        "title": data["title"],
        "url": data["url"],
        "webpage_url": data["webpage_url"],
        "duration": data.get("duration", 0),
        "thumbnail": data.get("thumbnail")
    }

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "default_search": "ytsearch",
    "extract_flat": False
}

FFMPEG_OPTIONS = {
    "before_options": (
        "-reconnect 1 "
        "-reconnect_streamed 1 "
        "-reconnect_delay_max 5"
    ),
    "options": "-vn"
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)