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
python trascript_podcasts.py --directory podcasts/the_bull --model base --device auto
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

- `--device`: Device to use for transcription (default: "auto")
  ```bash
  --device auto  # Options: auto, cpu, mps, cuda
  ```
  Available devices:
  - auto: Automatically selects the best available device
  - cpu: Forces CPU usage
  - mps: Uses Apple Metal Performance Shaders (M1/M2 Macs only)
  - cuda: Uses NVIDIA GPU (if available)

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
- On Apple Silicon Macs (M1/M2), the transcription will automatically use the Metal Performance Shaders (MPS) backend for faster processing when available
- The script processes files sequentially (one at a time) to ensure stability
- Temporary WAV files are created during processing and automatically cleaned up
- On Apple Silicon Macs (M1/M2/M3), the script will use CPU processing as faster-whisper doesn't support MPS (Metal Performance Shaders)
- For best performance on Mac, consider using a smaller model size (tiny or base)

