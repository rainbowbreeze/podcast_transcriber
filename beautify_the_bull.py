"""
This merger clean-up the text of the "The Bull - Il tuo podcast di finanza personale" podcast,
removing the advertising at the beginning and at the end of each episode.

It uses some keywords generally found in the transcription.

Update the strings if the clean-up is not satistying.
"""
import argparse
import logging
import re
from datetime import datetime
from typing import List
from pathlib import Path

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


def beaufity_and_merge_files(
    directory_path: str, 
    output_file_path: str
    ) -> None:
  """
  Find all trascript files in a directory, "beautify" the text and merge everything in a single file

  Args:
    directory_path: The path to the directory.
    output_file_path: The path of the destination file where the final text will be added

  Returns:
    None. The output is saved in the output file
  """
  try:
    path = Path(directory_path)

    # Delete the existing output file
    output_file = Path(output_file_path)
    if output_file.exists():
      output_file.unlink()
      output_file = None

    txt_files = [file_path for file_path in path.iterdir() if file_path.is_file() and ".txt" == file_path.suffix]
    txt_files.sort(key=lambda x: x.name)

    for file_path in txt_files:
        logger.debug(f"Processing {file_path.name}")

        with open(str(file_path), "r") as f:
          content: str = f.read()
        
        content = beautify_text(content, file_path.name)

        with open(output_file_path, 'a') as f:
          f.write(f"## {file_path.stem[11:]}")
          f.write('\n')
          
          # Extract date from filename and write it
          match = re.match(r'\[(\d{8})\]', file_path.name)
          if match:
              date_str = match.group(1)
              formatted_date = datetime.strptime(date_str, '%Y%m%d').strftime('Published on %Y-%m-%d')
              f.write(f"_{formatted_date}_  ")
              f.write('\n')

          f.write(content)
          f.write('\n')
          f.write('\n')
          f.write('\n')

  except FileNotFoundError:
    logger.error(f"Error: Directory '{directory_path}' not found.")



def beautify_text(
    source_text: str,
    file_name: str
    ) -> str:
  """
  Take a transcripted podcast text, and clean it up.

  Args:
    source_text: The text to beautify.
    file_name: The name of the file - only used for logging purposes
    
  Returns:
    str. The text improved.
  """

  # Check for initial parts to remove
  heads: List[str] = [
    "Il tuo podcast! Diffinanza personale",
    "Il tuo podcast! Di finanza personale!",
    "Il tuo podcast. Diffinanza personale",
    "Il tuo podcast Diffinanza personale",
    "Il tuo podcast di finanza personale!",
    "Il tuo podcast, di finanza personale",
    "Il tuo podcast di finanza personale",
    "Il tuo podcast, definanza personale",
    "Il tuo podcast, finanza personale",
    "Il tuo podcast, differenza personale",
    "Il tuo podcast. Di finanza personale",
    "Il tuo podcast. Definanza personale",
    "Il tuo podcast. Definitimola personalmente",
    "In tuo potcas, di finanza personale",
    "in tuo podcast di finanza personale",
    "Domanda da un miliardo di dollari oggi a The Bull"
  ]
  uppercase_source_text: str = source_text.upper()

  pos : int = -1
  for search_keyword in heads:
    pos = uppercase_source_text.find(search_keyword.upper())
    # > 2000 means the string was found at the closing of the podcast, not a the beginning
    if pos != -1 and pos < 2000:
      # Add the lenght of the searched keyword
      pos += len(search_keyword)
      # Add the additional punctiation mark and then the space
      pos += 2
      source_text = source_text[pos:]
      #logger.debug(f" Head \"{search_keyword}\" found at position {pos}")
      break
  
  if pos == -1 or pos > 2000:
    logger.info(f" ** Head - Nothing to clean-up for {file_name}")


  # Check for final parts to remove
  tails: List[str] = [
    "vi invito a mettere segui",
    "vi invito come sempre mettere",
    "vi invito come sempre a mettere",
    "a mettere segui attivare",
    "ricordo di mettere segui",
    "ricordo di cliccare su segui",
    "se metteste segui attivaste",
    "a mettere segui e attivare le notifiche",
    "metta segui e attivi",
    "mettere segui a attivare",
    "mettere segui attivare",
    "mettete seguite campanella",
    "mettete segui su Spotify",
    "mettete segui al podcast",
    "mettere segui al podcast",
    "mettete segui attivate le notifiche su",
    "Vi invito inoltre come sempre a mettere segui",
    "prima di chiudere avrete ancora una volta",
    "attivare le notifiche su Spotify",
    "attivi le notifiche su qualunque piattaforma",
    "cliccando su segui e attivando le notifiche",
    "cliccare su segui",
    "cliccare su Segui su Spotify o Apple Podcast",
    "Mi raccomando non smettete di seguirci",
    "un rating a 5 stelle",
    "lasciate una recensione a 5 stelle",
    "lasciare una recensione a 5 stelle",
    "metterebbe una recensione a 5 stelle",
    "mettete segui i 5 stelle",
    "Per il resto, spero che tutto questo vi sia piaciuto",
    "iscrivervi, mettere like ai video e attivare le notifiche",
    "Per questi episodi, invece, è davvero tutto",
    "Per questo episodio invece è davvero tutto",
    "Per il momento invece questo episodio finisce qui",
    "questo episodio per il momento finisce qui",
    "per questo episodio invece è davvero tutto",
    "Nel frattempo vi invito come sempre a mettere segui",
  ]
  uppercase_source_text: str = source_text.upper()

  for search_keyword in tails:
    pos: int = uppercase_source_text.find(search_keyword.upper())
    # < 20000 means the string was found at the closing of the podcast, not a the beginning
    if pos != -1 and pos > 15500:
      source_text = source_text[:pos]
      #logger.debug(f" Tail \"{search_keyword}\" found at position {pos}")
      break
  
  if pos == -1 or pos < 15500:
    logger.info(f" ** Tails - Nothing to clean-up for {file_name}")

  return source_text



def main() -> None:
  """
  Gets the directory path from the user and lists the files.
  """
  #directory_path: str = input("Enter the directory path: ")
  directory_path: str = "podcasts/the_bull"
  output_file_path: str = "podcasts/the_bull_total.md"
  beaufity_and_merge_files(directory_path, output_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge different podcast transcription files in a single file")

    # optional boolean parameter
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
        )
    args = parser.parse_args()

    # Set up logging with the specified level
    setup_logging(getattr(logging, args.log_level))

    main()
