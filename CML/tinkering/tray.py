import pystray
from PIL import Image, ImageDraw
import tomllib as tr

with open("config.toml", "rb") as f:
    config = tr.load(f)

def create_image():
    img = Image.new("RGB", (64, 64), color="blue")
    d = ImageDraw.Draw(img)
    d.rectangle((16, 16, 48, 48), fill="white")
    return img

def on_quit(icon, item):
    icon.stop()

tts_config = pystray.Menu(
    pystray.MenuItem("Enable TTS", None),
    pystray.MenuItem(f'Model: {config['tts']['model']}', None),
    pystray.MenuItem("", None)
)

config_menu = pystray.Menu(
    pystray.MenuItem("TTS", tts_config)
)

menu = pystray.Menu(
    pystray.MenuItem(f'{config["general"]["unique_id"]}', None),
    pystray.MenuItem("Config", config_menu),
    pystray.MenuItem("Quit", on_quit)
)

icon = pystray.Icon("TTL", create_image(), "TTL Tray", menu)
icon.run()