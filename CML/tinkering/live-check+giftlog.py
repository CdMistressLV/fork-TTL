import asyncio;
from TikTokLive import TikTokLiveClient;
from TikTokLive.client.logger import LogLevel;
from TikTokLive.events import ConnectEvent, GiftEvent;

client: TikTokLiveClient = TikTokLiveClient(
    unique_id="@cardmistresslive"
)

async def main():
    
    while (True):
        is_live = await client.is_live()
        
        if (not is_live):
            client.logger.info(
                "Client currently offline"
                "Reattempting in 30s"
            )
            await asyncio.sleep(30)
            continue
        
        client.logger.info("Client is Live, Connecting to livestream...")
        await client.connect()
        client.logger.info("Connected! Listening...")
        
        
        


