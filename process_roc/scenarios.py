from process_roc.preprocessing import prepare_data
from process_roc.calculator import calculate_roc_all_traces, calculate_roc_selected_traces, calculate_roc_single_trace
from process_roc.plotter import plot_traces

def scenario_1(log_file, case_id_column, delta_y, delta_x):
    """
    Scenario 1:
    Calculate the ROC for a all traces and generate an interactive plot.
    """

    df = prepare_data(log_file, case_id_column)
    
    all_traces_roc = calculate_roc_all_traces(df, delta_y=delta_y, delta_x=delta_x, 
                                              case_id_column=case_id_column)
    
    plot_traces(all_traces_roc, x_col=delta_x, y_col='ROC', 
                case_id_column=case_id_column, 
                title=f"ROC over {delta_x} for all Cases", y_axis_title="ROC")
    
    plot_traces(all_traces_roc, x_col=delta_x, y_col=delta_y, 
                case_id_column=case_id_column, 
                title=f"Velocity over {delta_x} for all Cases", y_axis_title="Velocity")

def scenario_2(log_file, case_id_column, delta_y, delta_x, selected_cases):
    """
    Scenario 2:
    Calculate the ROC for a set of selected traces and generate an interactive plot.
    """

    df = prepare_data(log_file, case_id_column)

    selected_traces_roc = calculate_roc_selected_traces(df, selected_cases=selected_cases,
                                                        delta_y=delta_y, 
                                                        delta_x=delta_x,
                                                        case_id_column=case_id_column)

    plot_traces(selected_traces_roc, x_col=delta_x, y_col='ROC',
                case_id_column=case_id_column,
                title=f"ROC over {delta_x} for Selected Cases: {', '.join(selected_cases)}",
                y_axis_title="ROC")
    
    plot_traces(selected_traces_roc, x_col=delta_x, y_col=delta_y, 
                case_id_column=case_id_column, 
                title=f"Velocity over {delta_x} for Selected Cases", y_axis_title="Velocity")

def scenario_3(log_file, case_id_column, delta_y, delta_x, case_id):
    """
    Scenario 3:
    Calculate the ROC for a single trace and generate an interactive plot.
    """
   
    df = prepare_data(log_file, case_id_column)

    single_trace_roc = calculate_roc_single_trace(df, case_id=case_id,
                                                  delta_y=delta_y,
                                                  delta_x=delta_x,
                                                  case_id_column=case_id_column)

    plot_traces(single_trace_roc, x_col=delta_x, y_col='ROC',
                case_id_column=case_id_column,
                title=f"ROC over {delta_x} for Case {case_id}", y_axis_title="ROC")

    plot_traces(single_trace_roc, x_col=delta_x, y_col=delta_y, 
                case_id_column=case_id_column, 
                title=f"Velocity over {delta_x} for Case {case_id}", y_axis_title="Velocity")