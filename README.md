# Talkie

A Python application for audio transcription using OpenAI's Whisper model.

## Features

- **File Transcription**: Transcribe audio files using Whisper
- **Live Audio Transcription**: Real-time transcription from microphone input
- **Voice Commands**: Stop recording by saying "stop"
- **Multiple Audio Formats**: Supports common audio formats (WAV, MP3, FLAC, etc.)

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync
```

### System Dependencies

On macOS, you'll need PortAudio for PyAudio:

```bash
brew install portaudio
```

## Usage

Start live audio transcription from your microphone:

```bash
uv run python transcribe.py
```

- The application will start recording from your default microphone
- Transcribed text appears with timestamps
- Say "stop" to end the recording session
- Press Ctrl+C to interrupt manually

## Configuration

### Whisper Models

You can use different Whisper models by modifying the `model_name` parameter:

- `tiny`: Fastest, least accurate
- `base`: Good balance of speed and accuracy (default)
- `small`: Better accuracy, slower
- `medium`: High accuracy, slower
- `large`: Best accuracy, slowest

### Audio Settings

The live transcriber uses these default settings:

- Sample rate: 16kHz
- Channels: Mono
- Chunk duration: 3 seconds
- Overlap: 25% between chunks

## Requirements

- Python 3.9+
- OpenAI Whisper
- PyAudio
- NumPy

See `pyproject.toml` for complete dependency list.
