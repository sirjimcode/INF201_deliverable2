from pathlib import Path
import re

# 1. Write a robust file reader function:


def read_log_file(file_path):

    """
   Funksjonen prøver først å lese filen med UTF-8-koding. Hvis det mislykkes, prøver den ISO-8859-1-koding.
   Den returnerer også en tuple.
    """
    path_obj = Path(file_path)

    try:
        content = path_obj.read_text(encoding='utf-8')
        encoding_used = 'utf-8'
    except UnicodeDecodeError:
        content = path_obj.read_text(encoding='iso-8859-1')
        encoding_used = 'iso-8859-1'

    return (content, encoding_used)


# 2. Write a log parser function that uses regular expressions.
# Log files contain valid sales lines mixed with system noise.
def parse_log_lines(log_innhold): 
