import pandas as pd
from pathlib import Path


RAW_FILE = Path("data/raw/superstore.csv")


def load_raw_data():
    """
    Load raw retail dataset.
    """

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_FILE}"
        )

    df = pd.read_csv(RAW_FILE)

    print("\nDataset loaded successfully.\n")

    return df