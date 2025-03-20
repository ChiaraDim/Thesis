import pandas as pd
from pandas import DataFrame
from typing import List, Optional, Union

def prepare_data(log_file: str, case_id_column: str) -> DataFrame:
    """
    Reads and prepares the log data for ROC calculations.

    Args:
        log_file (str): Path to the CSV log file.
        case_id_column (str): Name of the column identifying cases.

    Returns:
        DataFrame: Processed log dataframe with additional time features and frequency.
    """
    df = pd.read_csv(log_file)

    required_columns = [col for col in df.columns if 'case' in col.lower() or 'time' in col.lower()]
    if len(required_columns) < 2:
        raise ValueError("The log file does not contain the necessary columns to process.")

    timestamp_column = [col for col in df.columns if 'time' in col.lower() or 'timestamp' in col.lower()][0]

    df[timestamp_column] = pd.to_datetime(df[timestamp_column])

    df = df.dropna(subset=[timestamp_column])

    df = df.sort_values(by=[case_id_column, timestamp_column])

    df['timestamp_minutes'] = df.groupby(case_id_column)[timestamp_column] \
        .transform(lambda x: (x - x.min()).dt.total_seconds() / 60.0)

    df['rounded_time'] = df[timestamp_column].dt.floor('1D')

    frequency_over_time = df.groupby('rounded_time').size().reset_index(name='frequency')

    df = df.merge(frequency_over_time, how='left', on='rounded_time')

    return df
