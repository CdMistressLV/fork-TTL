import pystray
from PIL import Image, ImageDraw

def on_quit(icon, item):
    icon.stop()