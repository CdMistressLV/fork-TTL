import wave
from piper import PiperVoice
import winsound as ws

voice = PiperVoice.load(r"E:\Downloads\en_GB-cori-medium.onnx", r"E:\Downloads\en_GB-cori-medium.onnx.json")
with wave.open("piper.wav", "wb") as wav_file:
    voice.synthesize_wav("Its actually working!", wav_file)
    
ws.PlaySound("piper.wav", ws.SND_FILENAME)