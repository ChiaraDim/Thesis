import pandas as pd
from pandas import DataFrame
from typing import List
from process_roc.utils import log_discarded_events

def calculate_roc_single_trace(df: DataFrame, case_id: str, delta_y: str, delta_x: str, case_id_column: str) -> DataFrame:
    """
    Calculates the Rate of Change (ROC) for a single trace.

    Args:
        df (DataFrame): The prepared event log data.
        case_id (str): The identifier of the case to analyze.
        delta_y (str): The dependent variable (Y axis).
        delta_x (str): The independent variable (X axis).
        case_id_column (str): The name of the column that identifies each case.

    Returns:
        DataFrame: A DataFrame containing the ROC values for the specified trace.
    """
    trace_data = df[df[case_id_column] == case_id].sort_values(by=delta_x)

    duplicated_mask = trace_data.duplicated(subset=[delta_y, delta_x], keep='first')
    discarded_rows = trace_data[duplicated_mask]

    if not discarded_rows.empty:
        log_discarded_events(case_id, discarded_rows)

    trace_data = trace_data.drop_duplicates(subset=[delta_y, delta_x], keep='first').reset_index(drop=True)

    if pd.api.types.is_datetime64_any_dtype(trace_data[delta_x]):
        trace_data['ROC'] = trace_data[delta_y].diff() / (trace_data[delta_x].diff().dt.total_seconds() / 60)
    else:
        trace_data['ROC'] = trace_data[delta_y].diff() / trace_data[delta_x].diff()

    return trace_data[[case_id_column, delta_x, delta_y, 'ROC']]

def calculate_roc_all_traces(df: DataFrame, delta_y: str, delta_x: str, case_id_column: str) -> DataFrame:
    """
    Calculates the ROC for all traces in the event log.

    Args:
        df (DataFrame): The prepared event log data.
        delta_y (str): The dependent variable (Y axis).
        delta_x (str): The independent variable (X axis).
        case_id_column (str): The name of the column that identifies each case.

    Returns:
        DataFrame: A DataFrame containing the ROC values for all traces.
    """
    all_traces_roc = [
        calculate_roc_single_trace(df, case_id, delta_y, delta_x, case_id_column)
        for case_id in df[case_id_column].unique()
    ]
    return pd.concat(all_traces_roc, ignore_index=True)

def calculate_roc_selected_traces(df: DataFrame, selected_cases: List[str], delta_y: str, delta_x: str, case_id_column: str) -> DataFrame:
    """
    Calculates the ROC for a selected set of traces in the event log.

    Args:
        df (DataFrame): The prepared event log data.
        selected_cases (List[str]): List of case IDs to analyze.
        delta_y (str): The dependent variable (Y axis).
        delta_x (str): The independent variable (X axis).
        case_id_column (str): The name of the column that identifies each case.

    Returns:
        DataFrame: A DataFrame containing the ROC values for the selected traces.
    """
    selected_traces_roc = [
        calculate_roc_single_trace(df, case_id, delta_y, delta_x, case_id_column)
        for case_id in selected_cases
    ]
    return pd.concat(selected_traces_roc, ignore_index=True)
