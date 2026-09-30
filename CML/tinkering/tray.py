import pystray
import threading
import tomllib as tr
import tomli_w as tw
from tkinter import *
from tkinter import ttk
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
            
def write_and_close(subclass, name, var, root):
    global config
    config[subclass][name] = var.get()
    try:
        with open("config.toml", "w", encoding="utf-8") as f:
            f.write(tw.dumps(config))
    finally:
        root.destroy()
            
def variable_edit(subclass, name):
    def open_window():
        root = Tk()
    
        root.title("Editing variable")
    
        mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        var = StringVar(value=config[subclass][name])
        var_enter = ttk.Entry(mainframe, width=7, textvariable=var)
        var_enter.grid(column=1, row=2, sticky=(W, E))
    
        ttk.Label(mainframe, text=(f'Editing variable: {name}')).grid(column=1, row=1, sticky=(N, W))
    
        ttk.Button(mainframe, text="Save & Quit", command=lambda: write_and_close(subclass, name, var, root)).grid(column=1, row=4, sticky=W)
    
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=1)
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        
        var_enter.focus()
        root.bind("<Return>", lambda: write_and_close(subclass, name, var, root))
    
        root.mainloop()
    
    threading.Thread(target=open_window, daemon=True).start()
        
autocomm_config= pystray.Menu(
    pystray.MenuItem("Enable Autocomment", lambda: on_toggle("autocomment"))
)

model_config = pystray.Menu(
    pystray.MenuItem(f'Volume: {config["tts"]["volume"]}', lambda: variable_edit("tts", "volume")),
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