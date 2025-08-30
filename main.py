import whisper

def main():
    model = whisper.load_model("turbo")
    result = model.transcribe("jfk.flac")
    print(result["text"])

if __name__ == "__main__":
    main()


