from pandas import DataFrame

def validate_columns(df: DataFrame, required_columns: list) -> None:
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")