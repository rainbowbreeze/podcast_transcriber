# Requires Python <= 3.11.9
# openai-whisper doesn't support python > 3.11.9, so pip install openwai-whisper fails with python 3.13
#
# python3.11 -m venv .venv
# .venv/bin/activate
# pip install --upgrade pip
# pip install openai-whisper
#
# Same for SpeechRecognition[whisper-local]
#
#
# To download podcasts
# python -m podcast-downloader --config podcast-dowloader-config.json


from pathlib import Path

from pydub import AudioSegment
import speech_recognition as sr



def list_files_in_directory(directory_path: str) -> None:
  """
  Lists all files in the specified directory using pathlib.

  Args:
    directory_path: The path to the directory.

  Returns:
    None. Prints the names of the files in the directory.
  """
  try:
    path = Path(directory_path)
    for file_path in path.iterdir():
      if file_path.is_file() and ".mp3" == file_path.suffix:
        print(file_path.name)
        #print(file_path.stem)
        #print(file_path.suffix)

        # Search for the 
        transcript_file = file_path.with_suffix(".txt")
        if transcript_file.exists():
          print(f" - A file with name '{transcript_file.name}' already exists.")
        else:
           transcribe_mp3_to_text(str(file_path), str(transcript_file))

    #print(os.path.splitext(filename)[0])
    # Verify if the transcript file already exists
    #transcript_file_name: str = os.path.splitext(filename)[0]+ ".txt"

  except FileNotFoundError:
    print(f"Error: Directory '{directory_path}' not found.")


def transcribe_mp3_to_text(mp3_file_path: str, output_file_path: str) -> None:
    """
    Transcribes an MP3 audio file to a text file using the fast-whisper library.

    Args:
        mp3_file_path: The path to the MP3 file.
        output_file_path: The path to the output text file.

    Returns:
        None. Saves the transcribed text to the specified output file.
    """
    recognizer = sr.Recognizer()

    print(f" Start transcript of file '{mp3_file_path}'...")

    # Check if the file needs to be conversted in a wav file
    wav_file = Path(mp3_file_path).with_suffix(".wav")
    if not wav_file.exists():
        print(f" The file needs to be encoded in WAV format")
        encode_to_wav_file(mp3_file_path, str(wav_file))


    with sr.AudioFile(str(wav_file)) as source:
        audio = recognizer.record(source)

    try:
        # Use the default system recognizer (no cloud service)
        text = recognizer.recognize_whisper(audio, model="base")

        with open(output_file_path, "w") as f:
            f.write("** " + Path(mp3_file_path).stem + " **")
            f.write('\n')
            f.write(text)

        print(f" Transcription saved to {output_file_path}")
        wav_file.unlink()

    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Speech Recognition service; {e}")



def encode_to_wav_file(mp3_source_path: str, wav_dest_path:str) -> None:
    """
    Encode an MP3 audio file to a WAV audio file

    Args:
        mp3_source_path: The path to the MP3 file.
        wav_dest_path: The path to the output WAV file.

    Returns:
        None. Saves the transcribed text to the specified output file.
    """
    try: 
        source_audio = AudioSegment.from_mp3(mp3_source_path)
        print(f" File is long {source_audio.duration_seconds} seconds")
        source_audio.export(wav_dest_path, format="wav")
    except Exception as e:
        print(f"An expection occurred: {e}")
       

def main() -> None:
  """
  Gets the directory path from the user and lists the files.
  """
  #directory_path: str = input("Enter the directory path: ")
  directory_path = "podcasts/the_bull"
  list_files_in_directory(directory_path)

if __name__ == "__main__":
  main()
