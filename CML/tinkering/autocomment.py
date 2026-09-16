from TikTokLive import TikTokLiveClient
from TikTokLive.client.logger import LogLevel
import tomllib as tr

with open("config.toml", "rb") as f:
    config = tr.load(f)
    
async def main():
    client: TikTokLiveClient = TikTokLiveClient(config["general"]["unique_id"])
    
    client.web.set_session(
        config["general"]["sessionid"],
        config["general"]["ttl-tar-id"]
    )
    
    await client.connect()
    await client.send_room_chat("This is a test.")