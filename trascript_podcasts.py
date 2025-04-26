# Requires Python 3.11 or higher
# pip install SpeechRecognition[whisper-local]
# pip install pydub
# pip install tqdm

from pathlib import Path
from typing import List, Optional
import concurrent.futures
from tqdm import tqdm
import platform
import sys
import logging
import torch
from pydub import AudioSegment
import speech_recognition as sr
import time


# Global logger variable
logger = None


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


def get_device() -> str:
    """
    Determine the best device to use based on the system.
    Returns 'mps' for Apple Silicon, 'cuda' for NVIDIA GPUs, or 'cpu' otherwise.
    """
    try:
        if platform.system() == 'Darwin' and platform.processor() == 'arm':
            # Check if MPS is available and working
            if torch.backends.mps.is_available():
                # Test MPS with a simple operation
                try:
                    test_tensor = torch.randn(1, device='mps')
                    return 'mps'
                except Exception as e:
                    print(f"MPS device test failed: {e}. Falling back to CPU.")
                    return 'cpu'
        elif torch.cuda.is_available():
            return 'cuda'
    except Exception as e:
        print(f"Error checking device availability: {e}. Falling back to CPU.")
    
    return 'cpu'


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
        
        # Get the best available device
        device : str = get_device()
        logger.info(f"Using device: {device}")
        
        max_workers : int = 2 if device == 'mps' or device == 'cpu' else 1

        # When CUDA is used, it's better to process one file at time.
        # Instead, with CPU or MPS (with uses cpu because mps is not supported
        #  natively by whisper), it's more convenient to process 2 files in
        #  parallel. At least 15% to 20% faster in aggregate.
        # It means that, when happening in parallel, the time to perform a 
        #  transcription of a file is more than the time required to perform
        #  the same transcription with no concurrency.
        # But because more transcriptions are happening in parallel, at the end
        #  the whole process is faster, compared to when all the files are
        #  transcribed one after the other.
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for file_path in mp3_files:
                transcript_file = file_path.with_suffix(".txt")
                if not transcript_file.exists():
                    futures.append(executor.submit(transcribe_mp3_to_text, 
                                                 str(file_path), 
                                                 str(transcript_file),
                                                 model_size))
            
            # Show progress bar
            for future in tqdm(concurrent.futures.as_completed(futures), 
                             total=len(futures), 
                             desc="Transcribing files"):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error processing file: {e}")

    except FileNotFoundError:
        logger.error(f"Error: Directory '{directory_path}' not found.")


def transcribe_mp3_to_text(source_mp3_file_path: str, output_txt_file_path: str, model_size: str = "base") -> None:
    """
    Transcribes an MP3 audio file to a text file using SpeechRecognition with Whisper.

    Args:
        source_mp3_file_path: The path to the MP3 file.
        output_txt_file_path: The path to the output text file.
        model_size: The size of the Whisper model to use

    Returns:
        None. Saves the transcribed text to the specified output file.
    """
    logger.info(f"Starting transcription of '{Path(source_mp3_file_path).name}'...")

    try:
        # Convert MP3 to WAV if needed
        wav_file = Path(source_mp3_file_path).with_suffix(".wav")
        if not wav_file.exists():
            logger.info(f"Converting to WAV format...")
            encode_to_wav_file(source_mp3_file_path, str(wav_file))

        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Configure recognizer settings
        recognizer.energy_threshold = 300  # minimum audio energy to consider for recording
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8  # seconds of non-speaking audio before a phrase is considered complete
        
        with sr.AudioFile(str(wav_file)) as source:
            # Adjust for ambient noise
            logger.debug("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Record the audio
            logger.debug("Recording audio...")
            audio = recognizer.record(source)
            
            # Transcribe using Whisper
            logger.debug("Transcribing with Whisper...")
            start_time = time.time()
            text = recognizer.recognize_whisper(audio, 
                                              model=model_size,
                                              show_dict=False)
            time_for_transcription = time.time() - start_time
        
        # Write the transcription to file
        with open(output_txt_file_path, "w", encoding="utf-8") as f:
            f.write(f"** {Path(source_mp3_file_path).stem} **\n\n")
            f.write(text)

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
        source_audio = AudioSegment.from_mp3(mp3_source_path)
        logger.debug(f"File duration: {source_audio.duration_seconds:.0f} seconds")
        source_audio.export(wav_dest_path, format="wav")
    except Exception as e:
        logger.error(f"Error converting to WAV: {e}")
        raise


def main() -> None:
    """
    Main function to process podcast files.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Transcribe podcast episodes using SpeechRecognition with Whisper")
    parser.add_argument("--directory", help="Directory containing MP3 files")
    parser.add_argument("--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size to use")
    parser.add_argument("--log-level", default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                       help="Set the logging level")
    
    args = parser.parse_args()
    directory_path = "podcasts/the_bull"
    
    # Set up logging with the specified level
    setup_logging(getattr(logging, args.log_level))
    
    list_and_transcribe_files_in_directory(directory_path, args.model)


if __name__ == "__main__":
    main()
