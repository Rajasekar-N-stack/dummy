# recorder.py
import sounddevice as sd
import soundfile as sf
import threading
import queue
import numpy as np
import os

AUDIO_PATH = "audio/audio.wav"
FS = 16000  # Sample rate
CHANNELS = 1

q = queue.Queue()
recording = False
thread = None
all_chunks = []

def callback(indata, frames, time, status):
    q.put(indata.copy())

def start_recording():
    """
    Start recording audio (indefinitely) until manually stopped.
    """
    global recording, thread, all_chunks
    os.makedirs(os.path.dirname(AUDIO_PATH), exist_ok=True)
    recording = True
    all_chunks = []

    def _record():
        with sd.InputStream(samplerate=FS, channels=CHANNELS, callback=callback):
            while recording:
                try:
                    chunk = q.get(timeout=1)
                    all_chunks.append(chunk)
                except queue.Empty:
                    continue

    thread = threading.Thread(target=_record)
    thread.start()
    print("🎙️ Recording started...")

def stop_recording_and_save():
    """
    Stop recording and save the collected chunks to a .wav file.
    """
    global recording, all_chunks
    recording = False
    print("⏹️ Stopping recording...")

    if not all_chunks:
        print("⚠️ No audio recorded.")
        return None

    audio_data = np.concatenate(all_chunks, axis=0)
    sf.write(AUDIO_PATH, audio_data, FS)
    print(f"✅ Audio saved to: {AUDIO_PATH}")
    return AUDIO_PATH
