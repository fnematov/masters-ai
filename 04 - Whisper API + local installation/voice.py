import pyaudio
import wave
import keyboard
import time
from threading import Thread

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()


# Function to record audio
def record_audio(file_name):
    print("Recording...")
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    try:
        while keyboard.is_pressed("space"):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
    except KeyboardInterrupt:
        pass
    stream.stop_stream()
    stream.close()
    print(f"Recording stopped. Saving to {file_name}...")

    # Save recorded audio to a file
    with wave.open(file_name, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))


# Function to play audio
def play_audio(file_name):
    time.sleep(5)  # Wait for 5 seconds
    print(f"Playing {file_name}...")
    with wave.open(file_name, "rb") as wf:
        stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
    print("Playback finished.")


# Main loop
print("Press and hold the spacebar to record. Release to stop recording and playback.")
file_index = 1

try:
    while True:
        if keyboard.is_pressed("space"):
            file_name = f"recording_{file_index}.wav"
            record_thread = Thread(target=record_audio, args=(file_name,))
            record_thread.start()
            record_thread.join()  # Wait for recording to finish
            playback_thread = Thread(target=play_audio, args=(file_name,))
            playback_thread.start()
            file_index += 1
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    audio.terminate()