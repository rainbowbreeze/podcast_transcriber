## Project Overview

This project is a Python-based command-line tool for downloading and transcribing podcast episodes. It leverages several open-source libraries to achieve its functionality:

*   **`podcast-downloader`**: For downloading podcast episodes from an RSS feed.
*   **`pydub`**: For converting MP3 audio files to the WAV format required for transcription.
*   **`pywhispercpp`**: For transcribing the audio files to text using Whisper models.

The project is structured as a command-line application. All output and operations are handled through the terminal.

## Building and Running

### Setup

1.  **Create a virtual environment:**
    ```bash
    python3.11 -m venv .venv
    ```

2.  **Activate the virtual environment:**
    *   **Unix/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  **Download podcasts:**
    *   Configure the `podcast-downloader-config.json` file with the desired podcast RSS feed and download path.
    *   Run the following command to download new episodes:
        ```bash
        python -m podcast_downloader --config podcast-downloader-config.json
        ```

2.  **Transcribe podcasts:**
    *   Run the `transcript_podcasts.py` script with the following command, specifying the directory containing the downloaded MP3 files, the desired Whisper model, and the log level:
        ```bash
        python transcript_podcasts.py --directory podcasts/the_bull --model medium --log-level INFO
        ```

3.  **Merge and beautify transcripts:**
    *   Run the `file_merger.py` script to merge and clean up the generated transcript files:
        ```bash
        python file_merger.py
        ```

## Development Conventions

*   The project follows a functional programming paradigm where appropriate.
*   All code should be compatible with Python 3.11.
*   The `README.md` file should be kept in sync with any changes to the codebase.
*   The `GEMINI.md` file should be kept in sync with any changes to the codebase.
*   The project uses a `.gitignore` file to exclude virtual environments, and other non-essential files from version control.
*   Ensure all new functions and classes have comments.
*   DO NOT over engineer things. Start with the simplest implementation.
*   Always keep the performance and security as a first priority.
*   Ask for any clarification rather just guessing things if you are not clear about anything.

