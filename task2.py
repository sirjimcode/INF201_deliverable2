from pathlib import Path


def find_log_files(root_dir):
    """
    Søker gjennom rotmappen med en løkke og finner alle .log-filer, inkludert de i undermapper.
    Returnerer en liste med Path-objekter for hver funnet loggfil.
    """
    root_path = Path(root_dir)
    log_files = []

    # Sjekk at mappen faktisk finnes før vi starter
    if not root_path.exists() or not root_path.is_dir():
        return log_files

    for item in root_path.iterdir():
        if item.is_file() and item.suffix == ".log":
            # Fant en loggfil: legg til i listen
            log_files.append(item)
        elif item.is_dir():
            # Fant en undermappe: kall funksjonen rekursivt og slå sammen resultatene
            log_files.extend(find_log_files(item))

    return log_files
