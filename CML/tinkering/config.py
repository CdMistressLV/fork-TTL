import platform
import tomllib as tr
import tomli_w as tw
import os

config_path = "config.toml"

if not os.path.isfile(config_path):
    config = {
        "general": 
           {"platform": 0, "unique_id": 0, "sessionid": 0, "ttl-tar-id": 0, "tts": 1, "autocomment": 0},
        "tts": 
            {"model": 0, "volume": 0.5, "voice_variation": 1.0, "speaking_variation": 1.0, "speed": 2.0, "normalize_audio": False}
        }
    
    with open(config_path, "x") as f:
        f.write(config)
    
with open(config_path, "rb") as f:
    config = tr.load(f)

config.setdefault("general", {})
config.setdefault("tts", {})
config["general"].setdefault("platform", 0)
config["general"].setdefault("unique_id", 0)
config["general"].setdefault("sessionid", 0)
config["general"].setdefault("ttl-tar-id", 0)
config["general"].setdefault("tts", 1)
config["general"].setdefault("autocomment", 0)
config["tts"].setdefault("model", 0)
config["tts"].setdefault("volume", 0.5)
config["tts"].setdefault("voice_variation", 1.0)
config["tts"].setdefault("speaking_variation", 1.0)
config["tts"].setdefault("speed", 2.0)
config["tts"].setdefault("normalize_audio", False)

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