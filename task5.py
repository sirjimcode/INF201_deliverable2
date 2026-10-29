import json
from pathlib import Path

from task1 import parse_log_lines, read_log_file
from task2 import find_active_registers, find_log_files
from task3 import remove_price_outliers
from task4 import (
    calculate_item_refund_ratio,
    create_status_pivot_table,
    create_transaction_dataframe,
    resample_hourly_item_revenue,
)


def run_full_workflow(
    logs_dir: str | Path = "2026",
    registers_json_path: str | Path | None = "store_config.json",
    output_dir: str | Path = "output",
) -> None:
    """Kjører hele arbeidsflyten fra rålogg til ferdige rapporter (Steg 1-7)."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 1. Finner alle loggfiler i den angitte mappen (inkludert undermapper) og leser JSON-registerdata hvis gitt
    log_files = find_log_files(logs_dir)
    if not log_files:
        print("Ingen loggfiler funnet i den angitte mappen.")
        return

    active_registers: set[str] = set()
    if registers_json_path is not None and Path(registers_json_path).exists():
        with open(registers_json_path, encoding="utf-8") as json_file:
            json_data = json.load(json_file)
            active_registers = find_active_registers(json_data)

    # 2. Leser og parser hver loggfil, samler alle transaksjoner i en liste av dictionaries
    parsed_records: list[dict] = []
    for file_path in log_files:
        content, _ = read_log_file(file_path)
        records = parse_log_lines(content)
        parsed_records.extend(records)

    # 3. Bygger en Pandas DataFrame fra listen av dictionaries
    df = create_transaction_dataframe(parsed_records)

    # Filtrerer til kun aktive kasser hvis registerdata ble funnet
    if active_registers:
        df = df[df["register_id"].isin(active_registers)].copy()

    # 4. Bruker remove_price_outliers for å rense prisene
    df["price"] = remove_price_outliers(df["price"].to_numpy())

    # 5. konverterer NOK-priser til EUR ved å multiplisere med 10.0
    nok_mask = df["currency"] == "NOK"
    df.loc[nok_mask, "price"] *= 10.0

    # 6. Generererer rapporter: timebasert inntekt, status pivot-tabell og refusjonsforhold
    hourly_revenue = resample_hourly_item_revenue(df)
    status_pivot = create_status_pivot_table(df)
    refund_ratios = calculate_item_refund_ratio(df)

    # 7. Lagrer alle rapportene til CSV- og JSON-filer i output-mappen
    if active_registers:
        with open(output_path / "active_registers.txt", "w", encoding="utf-8") as f:
            for reg_id in sorted(active_registers):
                f.write(f"{reg_id}\n")

    df.to_csv(output_path / "cleaned_transactions.csv")
    hourly_revenue.reset_index().to_json(
        output_path / "hourly_revenue.json",
        orient="records",
        date_format="iso",
        indent=2,
    )
    status_pivot.to_csv(output_path / "status_pivot_table.csv")
    refund_ratios.to_csv(output_path / "item_refund_ratios.csv")


if __name__ == "__main__":
    # Tilpasserer stien til loggfiler og JSON-registerdata etter behov
    run_full_workflow(
        logs_dir="2026",
        registers_json_path="store_config.json",
        output_dir="output",
    )
