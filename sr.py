#!/usr/bin/env python3

import speech_recognition as sr
import time
import argparse

def transcribe_microphone_with_whisper(whisper_model="base"):
    """
    Transcribe audio from microphone using speech_recognition library with Whisper
    
    Args:
        whisper_model (str): Whisper model to use (tiny, base, small, medium, large)
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    
    print("Microphone calibrated. Ready to record.")
    print(f"Using Whisper model: {whisper_model}")
    print("Press Ctrl+C to exit\n")
    
    try:
        while True:
            print("Listening...")
            
            try:
                with microphone as source:
                    audio_data = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                print("Processing audio...")
                
                try:
                    text = recognizer.recognize_whisper(audio_data, model=whisper_model)
                    print(f"You said: {text}")
                    print("-" * 50)
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                    print("-" * 50)
                except sr.RequestError as e:
                    print(f"Error with Whisper service: {e}")
                    print("-" * 50)
                    
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                print(f"Error during recording: {e}")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\nExiting...")

def main():
    parser = argparse.ArgumentParser(description="Real-time microphone transcription with Whisper")
    parser.add_argument(
        "--model", 
        default="base", 
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model to use (default: base)"
    )
    
    args = parser.parse_args()
    
    print("Real-time Microphone Transcription with Whisper")
    print("=" * 50)
    
    try:
        sr.Microphone.list_microphone_names()
        print("Available microphones detected.")
    except Exception as e:
        print(f"Error accessing microphone: {e}")
        return
    
    transcribe_microphone_with_whisper(whisper_model=args.model)

if __name__ == "__main__":
    main()
