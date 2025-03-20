import pandas as pd
from pandas import DataFrame
from typing import List, Union, Optional

def calculate_roc_single_trace(df: DataFrame, case_id: str, delta_y: str, delta_x: str, case_id_column: str) -> DataFrame:
    trace_data = df[df[case_id_column] == case_id].sort_values(by=delta_x)
    trace_data = trace_data.drop_duplicates(subset=[delta_y, delta_x], keep='first').reset_index(drop=True)

    if delta_x == 'rounded_time':
        trace_data['ROC'] = trace_data[delta_y].diff() / (trace_data[delta_x].diff().dt.total_seconds() / 60)
    else:
        trace_data['ROC'] = trace_data[delta_y].diff() / trace_data[delta_x].diff()

    return trace_data[[case_id_column, delta_x, delta_y, 'ROC']]

def calculate_roc_all_traces(df: DataFrame, delta_y: str, delta_x: str, case_id_column: str) -> DataFrame:
    all_traces_roc = [
        calculate_roc_single_trace(df, case_id, delta_y, delta_x, case_id_column)
        for case_id in df[case_id_column].unique()
    ]
    return pd.concat(all_traces_roc, ignore_index=True)

def calculate_roc_selected_traces(df: DataFrame, selected_cases: List[str], delta_y: str, delta_x: str, case_id_column: str) -> DataFrame:
    selected_traces_roc = [
        calculate_roc_single_trace(df, case_id, delta_y, delta_x, case_id_column)
        for case_id in selected_cases
    ]
    return pd.concat(selected_traces_roc, ignore_index=True)