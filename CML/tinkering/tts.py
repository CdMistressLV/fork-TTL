import os
import wave
import time
import json
import tempfile
import tomllib as tr
from pathlib import Path
from typing import Optional
from piper import PiperVoice

with open("config.toml", "r", encoding="utf-8") as f:
    config = tr.load(f)
    
platform = config["general"]["platform"]
model = config["tts"]["model"]
model_config = (f"{model}.json")
voice = PiperVoice.load(model, model_config)

if platform == "Windows":
    import winsound as ws
elif platform == "Linux":
    import sounddevice as sd
    import soundfile as sf

def synthesize(text:str):
    with wave.open("piper.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

def playback():
    if platform == "Windows":
        ws.PlaySound("piper.wav", ws.SND_FILENAME)
    elif platform == "Linux":
        data, samplerate = sf.read("piper.wav")
        sd.play(data, samplerate)
        sd.wait()
        
def _acquire_lock(lock_path: Path, wait: float = 0.1, timeout: Optional[float] = None) -> bool:
    start = time.time()
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.close(fd)
            return True
        except FileExistsError:
            if timeout is not None and (time.time() - start) >= timeout:
                return False
            time.sleep(wait)

def _release_lock(lock_path: Path):
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass
    
def pop_first_jsonl_line(queue_path: Path, lock_path: Path) -> Optional[str]:
    acquired = _acquire_lock(lock_path, wait=0.05, timeout=5)
    if not acquired:
        return None
    try:
        if not queue_path.exists():
            return None
        with queue_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            return None
        first = lines[0]
        remaining = lines[1:]
        # write remaining to a temp file and atomically replace
        tmp = queue_path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            f.writelines(remaining)
        os.replace(str(tmp), str(queue_path))
        return first.strip()
    finally:
        _release_lock(lock_path)
        
def process_queue(queue_file: str = "comments.jsonl", poll_interval: float = 0.8):
    queue_path = Path(queue_file)
    lock_path = queue_path.with_suffix(".lock")

    while True:
        line = pop_first_jsonl_line(queue_path, lock_path)
        if not line:
            time.sleep(poll_interval)
            continue
        try:
            item = json.loads(line)
        except Exception:
            time.sleep(0.1)
            continue

        # adjust key name to match your JSONL format
        text = item.get("text") or item.get("comment") or str(item)
        tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp_wav.close()
        try:
            synthesize(text, tmp_wav.name)
            playback(tmp_wav.name)
        finally:
            try:
                os.unlink(tmp_wav.name)
            except OSError:
                pass
            
if __name__ == "__main__":
    process_queue("comments.jsonl", poll_interval=0.8)