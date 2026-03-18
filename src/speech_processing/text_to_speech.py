import os
from openai import api_key
import pyaudio
import time
from dotenv import load_dotenv
from deepgram import DeepgramClient, SpeakOptions
from playsound3 import playsound

load_dotenv()

class TTS:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.channels=1
        self.rate = 16000
        self.stream = self.audio.open(
            format = self.format,
            channels = self.channels,
            rate = self.rate,
            output=True
        )
    
    def speak(self, text):
      retries = 3
      while retries > 0:
        try:
            # STEP 1: Create a Deepgram client using the API key from environment variables   
            client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
            time.sleep(1)

            # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
            options = SpeakOptions(
                model="aura-asteria-en",
                encoding="linear16",
                container="none",
                sample_rate=16000
            )

            # STEP 3: Call the save method on the speak property
            SPEAK_OPTIONS = {"text": text}
            response = client.speak.v("1").stream({"text": text}, options)
            self.stream.write(response.stream.read())
            audio_data = response.stream.read()
            self.stream.write(audio_data)
            break

            # STEP 4: Play the audio file
            #if os.path.exists(self.filename):
               #playsound(self.filename)
            #else:
                #print("Audio file was not created.")

        except Exception as e:
            print(f"Connection Error: {e}. Retriying")
            retries-=1
            time.sleep(2)

    def close(self):
      if hasattr(self, 'stream'):
        self.stream.stop_stream()
        self.stream.close()
      self.audio.terminate()

if __name__ == "__main__":
    tts = TTS()
    tts.speak("Hello, how can I help you today?")