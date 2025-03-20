import argparse
from process_roc import scenarios

def main():
    parser = argparse.ArgumentParser(description="Process Mining ROC Analysis")
    parser.add_argument('--log_file', required=True, help='Path to the event log CSV')
    parser.add_argument('--case_id_column', required=True, help='Name of the case ID column (e.g. case:concept:name)')
    parser.add_argument('--delta_y', required=True, help='The dependent variable (Y axis), e.g., cumulative_cost')
    parser.add_argument('--delta_x', required=True, help='The independent variable (X axis), e.g., rounded_time or timestamp_minutes')
    parser.add_argument('--case_ids', nargs='*', help='Optional: List of case IDs to filter. Leave empty for all.')

    args = parser.parse_args()

    # No case IDs → scenario 1: all traces
    if not args.case_ids:
        scenarios.scenario_1(
            log_file=args.log_file,
            case_id_column=args.case_id_column,
            delta_y=args.delta_y,
            delta_x=args.delta_x
        )
    
    # Multiple case IDs → scenario 2
    elif len(args.case_ids) > 1:
        scenarios.scenario_2(
            log_file=args.log_file,
            case_id_column=args.case_id_column,
            delta_y=args.delta_y,
            delta_x=args.delta_x,
            selected_cases=args.case_ids
        )
    
    # Single case ID → scenario 3
    elif len(args.case_ids) == 1:
        scenarios.scenario_3(
            log_file=args.log_file,
            case_id_column=args.case_id_column,
            delta_y=args.delta_y,
            delta_x=args.delta_x,
            case_id=args.case_ids[0]
        )
    
    else:
        print("Invalid input combination! Please specify valid case IDs or none at all.")


if __name__ == "__main__":
    main()
