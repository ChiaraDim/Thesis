# Process ROC - Rate of Change Analysis for Process Mining

Chiara Di Marco Luketich (Universidad ORT, Uruguay)

## Project structure

```bash
 logs/                            # Contains input event logs (CSV and  XES files) used for analysis. 
 process_roc/
    ├── main.py                   # CLI entry point. 
    ├── scenarios.py              # Defines analysis scenarios: single trace, selected traces, or all traces.
    ├── preprocessing.py          # Data preparation and preprocessing functions.
    ├── calculator.py             # ROC calculation logic.
    ├── plotter.py                # Interactive visualization of ROC results using Plotly.
    └── utils.py                  # Utility functions for data validation and logging discarded events.
 metrics_roc/
    ├── cycleTime.py              # Cycle Time analysis integrated with ROC calculation.
    ├── throughputTime.py         # Throughput Time analysis integrated with ROC calculation.
    ├── idleTime.py               # Idle Time analysis integrated with ROC calculation.
    └── serviceTime.py            # Service Time analysis integrated with ROC calculation.
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Thesis.git
   cd Thesis
   ```

2. Install dependencies:
   ```bash
    pip install pandas==1.5.3
    pip install plotly==5.13.1
    pip install matplotlib==3.6.3
   ```
   Compatible with Python 3.8+.

## How to Use

Run the CLI by executing `main.py` from the terminal. The interface allows flexible configuration depending on the analysis scenario.
   ```bash
   python -m process_roc.main --log_file <path_to_log> --case_id_column <case_column> --value1 <y_axis_value> --value2 <x_axis_value> [--case_ids case1 case2 ...]
   ```

### Arguments Description

| Command | Description |
| --- | --- |
| `--log_file` | Path to the CSV file containing the event log to be analyzed (inside the `logs/` folder). |
| `--case_id_column` | Name of the column in the log that uniquely identifies each process instance (trace). |
| `--delta_y` | Dependent variable to be analyzed (Y-axis). |
| `--delta_x` | Independent variable (X-axis). |
| `--case_ids	` | List of case IDs to filter the analysis. If omitted, ROC will be computed for all cases. |


## Examples

### Scenario 1: ROC for all traces
  ```bash
    python -m process_roc.main \
        --log_file logs/orders_log.csv \
        --case_id_column case:concept:name \
        --value1 cumulative_cost \
        --value2 rounded_time
  ```

### Scenario 2: ROC for selected traces
```bash
python -m process_roc.main \
    --log_file logs/orders_log.csv \
    --case_id_column case:concept:name \
    --value1 cumulative_cost \
    --value2 rounded_time \
    --case_ids o-990009 o-990016 o-990002
```

### Scenario 3: ROC for a single trace
```bash
python -m process_roc.main \
    --log_file logs/orders_log.csv \
    --case_id_column case:concept:name \
    --value1 cumulative_cost \
    --value2 rounded_time \
    --case_ids o-990003
```

