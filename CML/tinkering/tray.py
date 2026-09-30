import pystray
import tomllib as tr
import tomli_w as tw
from PIL import Image, ImageDraw

with open("config.toml", "rb") as f:
    config = tr.load(f)

def create_image():
    img = Image.new("RGB", (64, 64), color="blue")
    d = ImageDraw.Draw(img)
    d.rectangle((16, 16, 48, 48), fill="white")
    return img

def on_quit(icon, item):
    icon.stop()
    
def on_toggle(value):
    if config["general"][value] == 1:
        config["general"][value] = 0
        with open("config.toml", "w", encoding="utf-8") as f:
            f.write(tw.dumps(config))
    else:
        config["general"][value] = 1
        with open("config.toml", "w", encoding="utf-8") as f:
            f.write(tw.dumps(config))
        
autocomm_config= pystray.Menu(
    pystray.MenuItem("Enable Autocomment", lambda: on_toggle("autocomment"))
)

model_config = pystray.Menu(
    pystray.MenuItem(f'Volume: {config["tts"]["volume"]}', None),
    pystray.MenuItem(f'Voice Variation: {config["tts"]["voice_variation"]}', None),
    pystray.MenuItem(f'Speaking Variation: {config["tts"]["speaking_variation"]}', None),
    pystray.MenuItem(f'Speed: {config["tts"]["speed"]}', None),
    pystray.MenuItem(f'Normalize Audio: {config["tts"]["normalize_audio"]}', None)
)

tts_config = pystray.Menu(
    pystray.MenuItem("Enable TTS", lambda: on_toggle("tts")),
    pystray.MenuItem(f'Model: {config['tts']['model']}', None),
    pystray.MenuItem("Voice Configuration", model_config)
)

config_menu = pystray.Menu(
    pystray.MenuItem("TTS", tts_config),
    pystray.MenuItem("Autocomment", autocomm_config)
)

menu = pystray.Menu(
    pystray.MenuItem(f'Username: {config["general"]["unique_id"]}', None),
    pystray.MenuItem("Config", config_menu),
    pystray.MenuItem("Quit", lambda: on_quit(icon, None))
)

icon = pystray.Icon("TTL", create_image(), "TTL Tray", menu)
icon.run()