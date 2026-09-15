import platform
import tomllib as tr
import tomli_w as tw
import os

config_path = "config.toml"

if not os.path.isfile(config_path):
    config = {"general": {"platform": 0, "unique_id": 0}, "tts": {"enabled": True, "model": 0}}
    with open(config_path, "x") as f:
        f.write(config)
    
with open(config_path, "rb") as f:
    config = tr.load(f)

config.setdefault("general", {})
config.setdefault("tts", {})
config["general"].setdefault("platform", 0)
config["general"].setdefault("unique_id", 0)
config["tts"].setdefault("enabled", True)
config["tts"].setdefault("model", 0)

if platform.system() == "Windows":
    config["general"]["platform"] = "Windows"
    with open("config.toml", "w", encoding="utf-8") as f:
        f.write(tw.dumps(config))

elif platform.system() == "Linux":
    config["general"]["platform"] = "Linux"
    with open("config.toml", "w", encoding="utf-8") as f:
        f.write(tw.dumps(config))
    
elif platform.system() == "Darwin":
    config["general"]["platform"] = "MacOS"
    with open("config.toml", "w", encoding="utf-8") as f:
        f.write(tw.dumps(config))