import numpy as np


def remove_price_outliers(price_data) -> np.ndarray:
    """
    Først konverterer input til en 1D NumPy float array. Deretter identifiserer og
    fjerner outliers basert på 3-sigma regelen. Outliers erstattes med medianen av de gyldige prisene.
    Returnerer en ny NumPy array med rensede priser.
    """
    # 1. Konverterer til 1D NumPy float array
    prices = np.array(price_data, dtype=float).flatten()

    # Hvis arrayet er tomt, returnerer det direkte
    if prices.size == 0:
        return prices

    # 2. Beregner gjennomsnittet (mu) og standardavviket (sigma)
    mu = np.mean(prices)
    sigma = np.std(prices)

    # 3. Boolsk maske for å identifisere outliers, det er verdier over tre standardavvik unna
    outlier_mask = np.abs(prices - mu) > (3 * sigma)

    # 4. Finner gyldige priser
    valid_prices = prices[~outlier_mask]

    # Hvis alle eller ingen verdier er outliers, trengs ingen erstatning
    if valid_prices.size == 0 or not np.any(outlier_mask):
        return prices

    # 5. Beregn medianen av de gyldige prisene
    valid_median = np.median(valid_prices)

    # 6. Klon arrayet (god praksis) og erstatt outliers med medianen
    cleaned_prices = prices.copy()
    cleaned_prices[outlier_mask] = valid_median

    return cleaned_prices


def compute_refund_ratio(sales_count: np.ndarray, refund_count: np.ndarray) -> np.ndarray:
    """
    Beregner forholdet mellom refusjoner og salg. For å unngå deling på null, legger vi til en liten epsilon-verdi.
    Returnerer en NumPy array med forholdet.
    """
    epsilon = 1e-6
    return refund_count / (sales_count + epsilon)
