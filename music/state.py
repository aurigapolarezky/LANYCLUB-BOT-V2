music_players = {}

def get_player(guild_id: int):
    if guild_id not in music_players:
        music_players[guild_id] = {
            "queue": [],
            "current": None,
            "loop": False,
            "loop_queue": False,
            "autoplay": False,
            "paused": False
        }
    return music_players[guild_id]