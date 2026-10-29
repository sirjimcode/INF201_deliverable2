import numpy as np
import pandas as pd
from task3 import compute_refund_ratio


def create_transaction_dataframe(transactions: list[dict]) -> pd.DataFrame:
    """
    Tar inn en liste med dictionaries som representerer transaksjoner og konverterer den til en Pandas DataFrame.
    """
    # 1. Konverterer listen med dictionaries til en DataFrame
    df = pd.DataFrame(transactions)

    # 2. Gjør om timestamp til datetime objekter
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 3. Setter timestamp som indeksen til tabellen
    df = df.set_index("timestamp")

    # 4. Sorter DataFramen kronologisk etter tidsstempel-indeksen
    df = df.sort_index()

    return df


def resample_hourly_item_revenue(df: pd.DataFrame) -> pd.Series:
    """
    Her tar funksjonen inn en DataFrame med transaksjoner og resampler
    den for å beregne total inntekt per vare per time.
    """
    return df.groupby('item').resample('1h')['price'].sum()


def create_status_pivot_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lager en Pivot-tabell som viser total inntekt per vare, gruppert etter status (SUCCESS, REFUND, CANCELLED).
    """
    pivot_df = df.pivot_table(
        values="price",
        index="item",
        columns="status",
        aggfunc="sum",
        fill_value=0.0,
    )

    return pivot_df


def calculate_item_refund_ratio(df: pd.DataFrame) -> pd.Series:
    """
    Beregner forholdet mellom antall refusjoner og antall salg for hver vare.
    Returnerer en Pandas Series med varenavn som indeks og forholdet som verdier.
    """
    # 1. Teller opp antall transaksjoner per vare og status
    counts = pd.crosstab(df["item"], df["status"])

    # 2. Henter ut antall vellykkede salg SUCCESS som et NumPy-array
    if "SUCCESS" in counts.columns:
        sales_count = counts["SUCCESS"].to_numpy()
    else:
        sales_count = np.zeros(len(counts))

    # 3. Hent ut antall refusjoner REFUND som et NumPy-array
    if "REFUND" in counts.columns:
        refund_count = counts["REFUND"].to_numpy()
    else:
        refund_count = np.zeros(len(counts))

    # 4. Kall funksjonen fra Task 3
    ratios = compute_refund_ratio(sales_count, refund_count)

    # 5. Returner som en Pandas Series koblet til varenavnene
    return pd.Series(ratios, index=counts.index, name="refund_ratio")
