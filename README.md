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

#### Optional Parameters
- `--directory`: Path to the directory containing MP3 files to transcribe (default: "podcasts/the_bull")
  ```bash
  --directory podcasts/the_bull
  ```

- `--model`: Whisper model size to use (default: "base")
  ```bash
  --model base  # Options: tiny, base, small, medium, large-v1, large-v2, large-v3
  ```
  Available model sizes:
  - tiny: Fastest but least accurate
  - base: Good balance of speed and accuracy
  - small: Better accuracy, slower
  - medium: Even better accuracy, slower
  - large: Best accuracy, slowest
More on available models at https://absadiki.github.io/pywhispercpp/#pywhispercpp.constants.AVAILABLE_MODELS .

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
- Time required to transcribe a file of 2558 seconds, in Italian, using only the CPU of a Mac M1 Pro
  - base: 202 secs
  - small: 555 secs
  - medium: 1503 secs
- Quality of the models:
  - The quality bump in the translation between base and small model is noticable, with small model way better than base model (more words translated, better puntuation, etc).
  - The quality bump in the translation between small and medium, altough noticable, doesn't impact significantly the final quality of the translation. Medium model captured a few specific words, while small model didn't, some more abbreviations and brand names, but the message is understandable.
- Temporary WAV files are created during processing in the podcasts directory, and automatically cleaned up if the translation was successful
- whisper models are downloaded under the `whisper_models` folder, instead of user folder


## Where to find podcasts
https://pod.link/ is a good start.  
Search for the podcast, open the Podcast Republic link, and in the Podcast Republic pace, copy the "Open the RSS" link. Use the link to configure the podcast source in the `podcast-downloader-config.json` file.