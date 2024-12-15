from typing import List
from pathlib import Path

def beaufity_and_merge_files(directory_path: str, output_file_path: str) -> None:
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

    for file_path in path.iterdir():
      if file_path.is_file() and ".txt" == file_path.suffix:
        print(f"Processing {file_path.name}")

        with open(str(file_path), "r") as f:
          content: str = f.read()
        
        content = beautify_text(content)

        with open(output_file_path, 'a') as f:
          f.write(file_path.stem)
          f.write('\n')
          f.write(content)
          f.write('\n')
          f.write('\n')

  except FileNotFoundError:
    print(f"Error: Directory '{directory_path}' not found.")



def beautify_text(source_text: str) -> str:
  """
  Take a transcripted podcast text, and clean it up.

  Args:
    source_text: The text to beautify.

  Returns:
    str. The text improve.
  """

  # Check for initial parts to remove
  heads: List[str] = [
    "Il tuo podcast! Diffinanza personale",
    "Il tuo podcast. Diffinanza personale",
    "Il tuo podcast Diffinanza personale",
    "Il tuo podcast, di finanza personale",
    "Il tuo podcast di finanza personale",
    "Il tuo podcast, definanza personale",
    "Il tuo podcast, finanza personale",
    "Il tuo podcast, differenza personale",
    "Il tuo podcast. Di finanza personale",
    "Il tuo podcast. Definanza personale",
  ]
  uppercase_source_text: str = source_text.upper()

  for search_keyword in heads:
    pos: int = uppercase_source_text.find(search_keyword.upper())
    # > 2000 means the string was found at the closing of the podcast, not a the beginning
    if pos != -1 and pos < 2000:
      # Add the lenght of the searched keyword
      pos += len(search_keyword)
      # Add the additional punctiation mark and then the space
      pos += 2
      source_text = source_text[pos:]
      #print(f" Found at position {pos}")
      break
  
  if pos == -1 or pos > 2000:
    print(f" ** Head - Nothing to clean-up...")


  # Check for final parts to remove
  tails: List[str] = [
    "invito a mettere segui",
    "invito come sempre mettere segui",
    "come sempre mettere segui",
    "a mettere segui attivare",
    "ricordo di mettere segui",
    "ricordo di cliccare su segui",
    "se metteste segui attivaste",
    "metta segui e attivi",
    "mettere segui a attivare",
    "mettere segui attivare",
    "mettete seguite campanella",
    "mettete segui su Spotify",
    "mettete segui al podcast",
    "mettere segui al podcast",
    "cliccando su segui e attivando le notifiche",
    "cliccare su segui",
    "un rating a 5 stelle",
    "lasciate una recensione a 5 stelle",
    "lasciare una recensione a 5 stelle",
    "metterebbe una recensione a 5 stelle",
    "mettete segui i 5 stelle"
  ]
  uppercase_source_text: str = source_text.upper()

  for search_keyword in tails:
    pos: int = uppercase_source_text.find(search_keyword.upper())
    # < 20000 means the string was found at the closing of the podcast, not a the beginning
    if pos != -1 and pos > 15500:
      source_text = source_text[:pos]
      #print(f" Found at position {pos}")
      break
  
  if pos == -1 or pos < 15500:
    print(f" ** Tails - Nothing to clean-up...")

  return source_text



def main() -> None:
  """
  Gets the directory path from the user and lists the files.
  """
  #directory_path: str = input("Enter the directory path: ")
  directory_path: str = "podcasts/the_bull"
  output_file_path: str = "podcasts/the_bull_total.txt"
  beaufity_and_merge_files(directory_path, output_file_path)


if __name__ == "__main__":
  main()
