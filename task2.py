from pathlib import Path


def find_log_files(root_dir):
    """
    Søker gjennom rotmappen med en løkke og rekursiv gjenkalling og finner alle .log-filer, inkludert de i undermapper.
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


def find_active_registers(data) -> set[str]:
    """
    En funksjon som leter gjennom en JSON-struktur (som kan være en ordbok eller en liste) og finner alle aktive kasser.
    Returnerer et sett med ID-er for aktive kasser.
    """
    active_ids = set()

    # Tilfelle 1: Vi står i en dictionary
    if isinstance(data, dict):
        # Sjekker om denne ordboken representerer en aktiv kasse
        if "id" in data and data.get("active") is True:
            active_ids.add(str(data["id"]))

        # Traverserer videre nedover ved alle verdier i ordboken
        for value in data.values():
            active_ids.update(find_active_registers(value))

    # Tilfelle 2: Vi står i en liste
    elif isinstance(data, list):
        # Traverserer hvert element i listen rekursivt
        for item in data:
            active_ids.update(find_active_registers(item))

    # Tilfelle 3 (Base case): primitive typer som int, str, bool
    # Gjør ingenting, dermed returnerer den bare det oppsamlede settet (eller et tomt sett)

    return active_ids
