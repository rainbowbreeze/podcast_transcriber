"""
This script transcribes all MP3 files in a specified directory using the pywhispercpp library.
It converts MP3 files to WAV format and then uses a Whisper model to generate the transcription.
"""
from pathlib import Path
import logging
from pydub import AudioSegment
from pywhispercpp.model import Model
import time
import argparse



# Global logger variable
logger : logging.Logger


def setup_logging(log_level=logging.INFO):
    """
    Set up logging configuration.
    
    Args:
        log_level: The logging level to use (default: INFO)
    """
    global logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)
    return logger


def list_and_transcribe_files_in_directory(directory_path: str, model_size: str = "base") -> None:
    """
    Lists all files in the specified directory and transcribes them.

    Args:
        directory_path: The path to the directory.
        model_size: The size of the Whisper model to use (tiny, base, small, medium, large)

    Returns:
        None. Prints the names of the files in the directory.
    """
    try:
        path = Path(directory_path)
        mp3_files = [file_path for file_path in path.iterdir() 
                    if file_path.is_file() and file_path.suffix == ".mp3"]
        
        if not mp3_files:
            logger.warning(f"No MP3 files found in {directory_path}")
            return

        logger.debug(f"Found {len(mp3_files)} MP3 total files")
        
        for file_path in mp3_files:
            transcript_file = file_path.with_suffix(".txt")
            if not transcript_file.exists():
                transcribe_mp3_to_text( 
                    str(file_path), 
                    str(transcript_file),
                    model_size
                )
        
    except FileNotFoundError:
        logger.error(f"Error: Directory '{directory_path}' not found.")


def transcribe_mp3_to_text(source_mp3_file_path: str, output_txt_file_path: str, model_size: str = "base") -> None:
    """
    Transcribes an MP3 audio file to a text file using pywhispercpp.

    Args:
        source_mp3_file_path: The path to the MP3 file.
        output_txt_file_path: The path to the output text file.
        model_size: The size of the Whisper model to use

    Returns:
        None. Saves the transcribed text to the specified output file.
    """
    logger.info(f"Starting transcription of '{Path(source_mp3_file_path).name}' using whisper.cpp library...")

    try:
        # Check if the whisper_models directory exists, and if not, create it
        # If no model dir is specified, files are automatically downloaded under
        #  ~/Library/Application Support/pywhispercpp/models

        models_dir = Path("whisper_models")
        if not models_dir.exists():
            logger.info(f"Creating directory for whisper models: {models_dir}")
            models_dir.mkdir()

        # Convert MP3 to WAV if needed
        wav_file = Path(source_mp3_file_path).with_suffix(".wav")
        if not wav_file.exists():
            logger.info(f"Converting to WAV format...")
            encode_to_wav_file(source_mp3_file_path, str(wav_file))

        # Available models at https://absadiki.github.io/pywhispercpp/#pywhispercpp.constants.AVAILABLE_MODELS
        # redirect_whispercpp_logs_to=False to see details of the model load, recognized processor and other parameters
        model = Model(model_size, models_dir=str(models_dir), redirect_whispercpp_logs_to=None)
        logger.debug("Transcribing with whisper.cpp...")
        start_time = time.time()

        segments = model.transcribe(str(wav_file), language=None, translate=False, print_progress=False)
        # Write the transcription to file
        with open(output_txt_file_path, "w", encoding="utf-8") as f:
            f.write(f"** {Path(source_mp3_file_path).stem} **\n\n")

            for segment in segments:
                f.write(segment.text)
                f.write(" ")

        time_for_transcription = time.time() - start_time
        logger.info(f"Transcription completed in {time_for_transcription:.0f} seconds and saved to {output_txt_file_path}")
        
        # Clean up WAV file
        wav_file.unlink()

    except Exception as e:
        logger.error(f"Error processing {source_mp3_file_path}: {str(e)}")
        raise

def encode_to_wav_file(mp3_source_path: str, wav_dest_path: str) -> None:
    """
    Encode an MP3 audio file to a WAV audio file

    Args:
        mp3_source_path: The path to the MP3 file.
        wav_dest_path: The path to the output WAV file.

    Returns:
        None. Saves the WAV file to the specified path.
    """
    try: 
        # Load the mp3 file
        audio = AudioSegment.from_mp3(mp3_source_path)
        logger.debug(f"File duration: {audio.duration_seconds:.0f} seconds")
        # Set the frame rate to 16000 Hz (16 kHz)
        audio = audio.set_frame_rate(16000)
        # Set the number of channels to 1 (mono) - good practice for speech recognition, to simplify the audio data
        audio = audio.set_channels(1)
        # Export the result as a wave file
        audio.export(wav_dest_path, format="wav")
    except Exception as e:
        logger.error(f"Error converting to WAV: {e}")
        raise


def main() -> None:
    """
    Main function to process podcast files.
    """
    
    parser = argparse.ArgumentParser(
        description="This script transcribes all MP3 files in a specified directory using the pywhispercpp library."
    )
    parser.add_argument(
        "--directory",
        default="podcasts/the_bull",
        help="Directory containing MP3 files"
        )
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"],
        help="Whisper model size to use"
        )
    parser.add_argument(
        "--log-level", default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
        )
    
    args = parser.parse_args()
    
    # Set up logging with the specified level
    setup_logging(getattr(logging, args.log_level))
    
    list_and_transcribe_files_in_directory(args.directory, args.model)


if __name__ == "__main__":
    main()
