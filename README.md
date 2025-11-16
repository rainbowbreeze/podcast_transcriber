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
You first need mp3 files with podcast episodes to transcribe.  
If you already have, put them in a folder under this project. For example `podcasts/my_preferred_podcasts/`.  
Otherwise, the module [podcast_downloader](https://github.com/dplocki/podcast-downloader) can download podcasts episodes for you. This projects provide an example config file to download all the episodes from an existing podcast.
```bash
python -m podcast_downloader --config podcast-downloader-config.json
```
If the script is relauched, only new episodes are downloaded.  

Where to find podcasts:
- https://pod.link/ is a good start.  
- Search for the podcast, open the `Podcast Republic` link, and in the Podcast Republic page, copy the "Open the RSS" link.
- Use the link to configure the podcast source in the `podcast-downloader-config.json` file.



### Transcribing Podcasts

The podcast transcription is done using [pywhispercpp](https://github.com/abdeladim-s/pywhispercpp), and should be able to leverage GPU on different systems.
```bash
python transcript_podcasts.py --directory podcasts/the_bull --model medium --log-level INFO
```

Language of the podcast is automatically detected, so it works with all the languages supported by whisper.  
It could be possible to force the automatic translation and transcription to a particular language, but the Model class needs to be configured in code.



### Command Line Parameters

#### Optional Parameters
- `--directory`: Path to the directory containing MP3 files to transcribe (default: "podcasts/the_bull")
  ```bash
  --directory podcasts/the_bull
  ```

- `--model`: Whisper model size to use (default: "base")
  ```bash
  --model mediumn  # Options: tiny, base, small, medium, large-v1, large-v2, large-v3
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
- Time required to transcribe a file of 2558 seconds, in Italian, using the GPU of a Mac M1 Pro
  - medium: 264 secs
- Quality of the models:
  - The quality bump in the translation between base and small model is noticable, with small model way better than base model (more words translated, better puntuation, etc).
  - The quality bump in the translation between small and medium, altough noticable, doesn't impact significantly the final quality of the translation. However, medium model captured a few specific words, while small model didn't, some more abbreviations and brand names, but the message is understandable.
  - So, **my reccommendation** is to use small model, if only CPU is available: it does its job with minor issues. Otherwise, if a GPU is available, or a good quality of the transcription is needed, or time is not an issue, use the medium model.
- Temporary WAV files are created during processing in the podcasts directory, and automatically cleaned up if the translation was successful
- whisper models are downloaded under the `whisper_models` project folder, instead of user folder.
  - change it in the code if you prefer to use shared models across different apps using whispercpp module.



## Acknowledgements

This project utilizes the following amazing open-source libraries:

*   [podcast-downloader](https://github.com/dplocki/podcast-downloader): For downloading podcast episodes.
*   [pydub](https://github.com/jiaaro/pydub): For audio manipulation, such as converting MP3 to WAV.
*   [pywhispercpp](https://github.com/abdeladim-s/pywhispercpp): For efficient and accurate audio transcription using Whisper models.



## License

Project released under [GNU GPL 3](LICENSE).
