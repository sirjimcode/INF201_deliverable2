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
    """
    Splitter linjene, deretter itererer hver linje for å finne de 6 nøkleverdiene: timestamp,
    register_id, item, price, currency og status. Returnerer en liste med ordbøker som representerer hver transaksjon
    i mønstret som er definert i regexen. Hvis en linje ikke samsvarer med mønsteret, ignoreres den.
    """
    pattern = (
        r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
        r"\[(.*?)\] "
        r"item=(.*?) "
        r"price=([\d.]+) "
        r"([A-Z]{3}) "
        r"\((SUCCESS|REFUND|CANCELLED)\)$"
    )
    transactions = []
    for line in log_innhold.splitlines():
        line = line.strip()
        match = re.search(pattern, line)
        if match:
            record = {
                "timestamp": match.group(1),
                "register_id": match.group(2),
                "item": match.group(3),
                "price": float(match.group(4)),
                "currency": match.group(5),
                "status": match.group(6)
            }
            transactions.append(record)
    return transactions
