from datetime import datetime
from TikTokLive.client.client import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
import tomllib as tr
import os
import json
import asyncio

LOG_FILE = ("comments.jsonl")

if not os.path.isfile(LOG_FILE):
    with open(LOG_FILE, "x") as f:
        f.write("")

with open("config.toml", "rb") as f:
    config = tr.load(f)


client: TikTokLiveClient = TikTokLiveClient(
    unique_id=config["general"]["unique_id"]
)

ONLY_NEW_COMMENTS: bool = True # If True, comments TikTok delivers as backlog (posted before this script connected) are dropped.
connected_at_ms: int = 0


@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    global connected_at_ms
    connected_at_ms = int(datetime.now().timestamp() * 1000)
    client.logger.info(f"Connected to @{event.unique_id}!")


@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    if ONLY_NEW_COMMENTS and event.common.create_time < connected_at_ms:
        return

    entry = {
        "iso_ts": datetime.fromtimestamp(event.common.create_time / 1000).isoformat(),
        "create_time_ms": event.common.create_time,
        "nickname": event.user.nickname,
        "comment": event.comment
    }
    
    def _append(entry_obj):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry_obj, ensure_ascii=False) + "\n")

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _append, entry)


if __name__ == '__main__':
    client.run()
