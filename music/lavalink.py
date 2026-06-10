import os
import wavelink

async def connect_lavalink(bot):

    await wavelink.Pool.connect(
        nodes=[
            wavelink.Node(
                uri=f"https://{os.getenv('LAVALINK_HOST')}",
                password=os.getenv("LAVALINK_PASSWORD")
            )
        ],
        client=bot
    )

    print("✅ Connected to Lavalink!")