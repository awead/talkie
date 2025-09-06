import numpy as np
import pyaudio
import queue
import threading
import time
import whisper

class LiveTranscriber:


    def __init__(self, model_name="base", chunk_duration=3.0):
        """
        
        """
        self.model = whisper.load_model(model_name)
        self.chunk_duration = chunk_duration
        self.sample_rate = 16000
        self.chunk_size = int(self.sample_rate * self.chunk_duration)
        self.audio_queue = queue.Queue()
        self.is_recording = False
        
        # PyAudio configuration
        self.format = pyaudio.paInt16
        self.channels = 1
        self.audio = pyaudio.PyAudio()
        

    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback function for PyAudio stream"""
        if self.is_recording:
            self.audio_queue.put(in_data)
        return (None, pyaudio.paContinue)
    

    def record_audio(self):
        """Start recording audio stream"""
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=1024,
            stream_callback=self.audio_callback
        )
        
        print("🎤 Recording started... Press Ctrl+C to stop")
        stream.start_stream()
        
        try:
            while self.is_recording:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            stream.stop_stream()
            stream.close()
    

    def process_audio_chunks(self):
        """Process audio chunks and transcribe them"""
        audio_buffer = b''
        
        while self.is_recording:
            try:
                chunk = self.audio_queue.get(timeout=1.0)
                audio_buffer += chunk
                
                if len(audio_buffer) >= self.chunk_size * 2:
                    # Convert/normalize audio
                    audio_data = np.frombuffer(audio_buffer, dtype=np.int16)
                    audio_data = audio_data.astype(np.float32) / 32768.0
                    
                    # Transcribe the audio chunk
                    self.transcribe_chunk(audio_data)
                    
                    # Keep some overlap for context (25% overlap)
                    overlap_size = self.chunk_size // 4 * 2
                    audio_buffer = audio_buffer[-overlap_size:]
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Error processing audio: {e}")
    

    def transcribe_chunk(self, audio_data):
        """
        Transcribe a single audio chunk using Whisper

        Whisper will output frame logging information to STDERR. You can remove that with:
            uv run python transcribe.py 2>/dev/null

        Later we can redirect to a file using the io library.
        """
        try:
            result = self.model.transcribe(
                audio_data,
                language="en",
                task="transcribe",
                fp16=False,
                verbose=False
            )
            
            # Extract text and filter out empty/noise
            text = result["text"].strip()
            if text and len(text) > 2:
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] {text}")
                
                # Check for stop command
                if "stop" in text.lower():
                    self.stop()

        except Exception as e:
            print(f"❌ Transcription error: {e}")
    

    def start(self):
        """Start live transcription"""
        self.is_recording = True
        
        # Start audio recording thread
        record_thread = threading.Thread(target=self.record_audio)
        record_thread.daemon = True
        record_thread.start()
        
        # Start audio processing thread
        process_thread = threading.Thread(target=self.process_audio_chunks)
        process_thread.daemon = True
        process_thread.start()
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("🛑 received keyboard interrupt...")
            self.stop()
    

    def stop(self):
        """Stop recording and transcription"""
        if not self.is_recording:
            return

        self.is_recording = False
        self.audio.terminate()
        print("✅ Transcription stopped")


def main():
    print("🎙️  Live Audio Transcription with Whisper")
    print("=" * 50)
    
    transcriber = LiveTranscriber(model_name="base", chunk_duration=3.0)
    
    try:
        transcriber.start()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        transcriber.stop()

if __name__ == "__main__":
    main()
