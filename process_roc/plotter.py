import plotly.graph_objects as go
from pandas import DataFrame

def plot_traces(df: DataFrame, x_col: str, y_col: str, case_id_column: str, title: str, y_axis_title: str, x_axis_type: str = "linear") -> None:
    fig = go.Figure()

    for case_id in df[case_id_column].unique():
        trace_data = df[df[case_id_column] == case_id].dropna(subset=[y_col])
        if trace_data.empty:
            continue

        fig.add_trace(go.Scatter(
            x=trace_data[x_col],
            y=trace_data[y_col],
            mode='lines+markers',
            name=f'Case {case_id}'
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_axis_title,
        legend_title="Case ID",
        template="plotly_white"
    )

    fig.show()