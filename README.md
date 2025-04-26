# podcast_transcriber
Transcribe the episodes of a podcast

## Requirements
- Python 3.11 or 3.12 (as of April 2025, does not work with Python 3.13)
- Virtual environment (recommended)

## Setup
```bash
# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Downloading Podcasts
```bash
python -m podcast_downloader --config podcast-downloader-config.json
```

### Transcribing Podcasts
```bash
python trascript_podcasts.py --directory podcasts/the_bull --model base
```

### Command Line Parameters

#### Required Parameters
- `--directory`: Path to the directory containing MP3 files to transcribe
  ```bash
  --directory podcasts/the_bull
  ```

#### Optional Parameters
- `--model`: Whisper model size to use (default: "base")
  ```bash
  --model base  # Options: tiny, base, small, medium, large
  ```
  Available model sizes:
  - tiny: Fastest but least accurate
  - base: Good balance of speed and accuracy
  - small: Better accuracy, slower
  - medium: Even better accuracy, slower
  - large: Best accuracy, slowest

- `--log-level`: Set the logging level (default: "INFO")
  ```bash
  --log-level INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
  ```
  Available log levels:
  - DEBUG: Detailed information for debugging
  - INFO: General information about program execution
  - WARNING: Warning messages for potential issues
  - ERROR: Error messages for serious problems
  - CRITICAL: Critical errors that may prevent program execution

## Notes
- The script processes files sequentially (one at a time) on CUDA-enabled hardware, and with two tasks in paralled on cpu or mps hardware
  - More info on the reasons are available as comments in the code
- On Apple Silicon Macs (M1/M2/M3), the script will use CPU processing as faster-whisper doesn't support MPS (Metal Performance Shaders)
- For best performance on Mac, consider using a smaller model size (base or small)
  - Time required to transcribe a file of 2558 seconds, in Italian
    - base:
    - small: 555 secs
    - medium: 1503 secs
  - The quality bump in the translation between base and small model, is noticable, with small model way better than base model (more words translated, better puntuation, etc).
  - The quality bump in the translation between small and medium, altough noticable, doesn't impact significantly the final quality of the translation. A few specific words medium model captured, while small model didn't, but the message is understandable.
- On MacOS, Whisper downloads its models under  ~/.cache/whisper/
- Temporary WAV files are created during processing in the podcasts directory, and automatically cleaned up if the translation was successful

