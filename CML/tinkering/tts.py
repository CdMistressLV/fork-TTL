import wave
from piper import PiperVoice
import tomllib as tr

with open("config.toml", "r", encoding="utf-8") as f:
    config = tr.load(f)
    
platform = config["general"]["platform"]

if platform == "Windows":
    import winsound as ws
elif platform == "Linux":
    import sounddevice as sd
    import soundfile as sf

def comment_speak(text: str, platform: str = platform):
    voice = PiperVoice.load(r"E:\Downloads\en_GB-cori-medium.onnx", r"E:\Downloads\en_GB-cori-medium.onnx.json")
    with wave.open("piper.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    if platform == "Windows":
        ws.PlaySound("piper.wav", ws.SND_FILENAME)
    elif platform == "Linux":
        data, samplerate = sf.read("piper.wav")
        sd.play(data, samplerate)
        sd.wait()