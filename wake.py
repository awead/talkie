import pyaudio
import numpy as np
from wake_word_detector import WakeWordDetector

def main():
    # Audio configuration
    CHUNK = 1280  # 80ms at 16kHz (required by openwakeword)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    # Initialize wake word detector
    detector = WakeWordDetector(wake_words=["minerva"])
    
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    
    try:
        # Open audio stream
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        print("Listening for wake words... Press Ctrl+C to stop")
        
        while True:
            # Read audio chunk
            data = stream.read(CHUNK)
            
            # Convert to numpy array
            audio_chunk = np.frombuffer(data, dtype=np.int16)
            
            # Detect wake word
            wake_word = detector.detect(audio_chunk)
            
            if wake_word:
                print(f"Wake word detected: {wake_word}")
                
    except KeyboardInterrupt:
        print("\nStopping wake word detection...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        audio.terminate()

if __name__ == "__main__":
    main()
