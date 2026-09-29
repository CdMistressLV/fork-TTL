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

model_config = pystray.Menu(
    pystray.MenuItem(f'Volume: {config["tts"]["volume"]}', None),
    pystray.MenuItem(f'Voice Variation: {config["tts"]["voice_variation"]}', None),
    pystray.MenuItem(f'Speaking Variation: {config["tts"]["speaking_variation"]}', None),
    pystray.MenuItem(f'Speed: {config["tts"]["speed"]}', None),
    pystray.MenuItem(f'Normalize Audio: {config["tts"]["normalize_audio"]}', None)
)

tts_config = pystray.Menu(
    pystray.MenuItem("Enable TTS", None),
    pystray.MenuItem(f'Model: {config['tts']['model']}', None),
    pystray.MenuItem("", None),
    pystray.MenuItem("Voice Configuration", model_config)
)

config_menu = pystray.Menu(
    pystray.MenuItem("TTS", tts_config)
)

menu = pystray.Menu(
    pystray.MenuItem(f'Username: {config["general"]["unique_id"]}', None),
    pystray.MenuItem("Config", config_menu),
    pystray.MenuItem("Quit", on_quit)
)

icon = pystray.Icon("TTL", create_image(), "TTL Tray", menu)
icon.run()