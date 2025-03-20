import pandas as pd
from pandas import DataFrame
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def validate_columns(df: DataFrame, required_columns: list) -> None:
    """
    Validates that the required columns exist in the dataframe.

    Raises:
        ValueError: If any required columns are missing.
    """
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

def log_discarded_events(case_id: str, discarded_rows: DataFrame, reason: str = "Duplicated delta_x and delta_y", output_filename: str = "discarded_events.csv") -> None:
    """
    Logs discarded events to a CSV file for traceability.

    Args:
        case_id (str): The ID of the case being processed.
        discarded_rows (DataFrame): DataFrame containing the discarded events.
        reason (str): Reason why these events were discarded.
        output_file (str): Path to the CSV file where discarded events are logged.
    """
    if discarded_rows.empty:
        return

    discarded_rows = discarded_rows.copy()
    discarded_rows['discard_reason'] = reason
    discarded_rows['discard_case_id'] = case_id

    output_path = BASE_DIR / output_filename

    if not output_path.exists():
        discarded_rows.to_csv(output_path, index=False)
    else:
        discarded_rows.to_csv(output_path, mode='a', header=False, index=False)
