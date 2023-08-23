from flask import Flask, render_template
import schedule
import time
import threading
import sounddevice as sd
import os
import datetime

app = Flask(__name__)

# Directory to store audio recordings
AUDIO_DIR = os.path.join(app.root_path, "audio_recordings")

def access_microphone():
    print("Accessing microphone...")
    fs = 44100  # Sample rate
    seconds = 5  # Duration of audio capture

    # Capture audio from the microphone
    audio_data = sd.rec(int(fs * seconds), samplerate=fs, channels=1)
    sd.wait()  # Wait for the capture to complete

    # Save audio to a file
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_path = os.path.join(AUDIO_DIR, f"{timestamp}.wav")
    sd.write(file_path, audio_data, fs)
    print(f"Saved audio to: {file_path}")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    schedule.every().day.at("09:00").do(access_microphone)
    schedule.every().day.at("13:00").do(access_microphone)
    schedule.every().day.at("18:00").do(access_microphone)

    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

    app.run(host='0.0.0.0', port=5000)
