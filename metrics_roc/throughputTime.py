import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -------------------------------------------------------
#                    THROUGHPUT TIME
# -------------------------------------------------------

log_file = "logs/orders_log.csv"
event_log = pd.read_csv(log_file)

event_log['Timestamp'] = pd.to_datetime(event_log['time:timestamp'], errors='coerce')

throughput_times = (event_log.groupby('case:concept:name')['Timestamp']
                        .agg(StartTimestamp='min', EndTimestamp='max')
                        .reset_index())

throughput_times['ThroughputTime (hours)'] = (
    (throughput_times['EndTimestamp'] - throughput_times['StartTimestamp'])
    .dt.total_seconds() / 3600
)

throughput_times['Date'] = throughput_times['EndTimestamp'].dt.date
daily_throughput = (throughput_times.groupby('Date')
                    .agg(TotalThroughputTime=('ThroughputTime (hours)', 'sum'),
                         NumberOfCases=('ThroughputTime (hours)', 'count'))
                    .reset_index())

daily_throughput['AverageThroughputTime'] = (
    daily_throughput['TotalThroughputTime'] / daily_throughput['NumberOfCases']
)

daily_throughput['ROC'] = daily_throughput['AverageThroughputTime'].diff()

# ............................................................

# Define anomalous periods
anomalous_periods = [
    ('2023-08-01 00:00:00+00:00', '2023-09-30 23:59:59+00:00'),
    ('2023-11-01 00:00:00+00:00', '2023-12-31 23:59:59+00:00'),
    ('2024-04-01 00:00:00+00:00', '2024-05-30 23:59:59+00:00'),
    ('2024-05-01 00:00:00+00:00', '2024-06-30 23:59:59+00:00')   
]

filtered_logs = []
for start, end in anomalous_periods:
    filtered_logs.append(event_log[(event_log['Timestamp'] >= pd.Timestamp(start)) &
                                   (event_log['Timestamp'] <= pd.Timestamp(end))])
anomalous_log = pd.concat(filtered_logs)

print("Filtered Event Log for Anomalous Periods:")
print(anomalous_log.head())

# ............................................................

# Define normal periods
normal_periods = [
    ('2023-04-01 00:00:00+00:00', '2023-05-30 23:59:59+00:00'),
    ('2023-06-01 00:00:00+00:00', '2023-07-31 23:59:59+00:00'),
    ('2023-12-01 00:00:00+00:00', '2024-01-30 23:59:59+00:00'),
    ('2024-02-01 00:00:00+00:00', '2024-03-30 23:59:59+00:00')   
]

filtered_logs = []
for start, end in normal_periods:
    filtered_logs.append(event_log[(event_log['Timestamp'] >= pd.Timestamp(start)) &
                                   (event_log['Timestamp'] <= pd.Timestamp(end))])
normal_periods = pd.concat(filtered_logs)

print("Filtered Event Log for Normal Periods:")
print(normal_periods.head())

# ............................................................

# Group by Activity - Anomalous Periods
activity_analysis = anomalous_log.groupby('concept:name').agg(
    TotalDuration=('Timestamp', lambda x: (x.max() - x.min()).total_seconds() / 3600),
    Frequency=('concept:name', 'count')
).sort_values(by='Frequency', ascending=False)

print("Activity Analysis During Anomalous Periods:")
print(activity_analysis)

# Group by Activity - Normal Periods
activity_analysis_n = normal_periods.groupby('concept:name').agg(
    TotalDuration=('Timestamp', lambda x: (x.max() - x.min()).total_seconds() / 3600),
    Frequency=('concept:name', 'count')
).sort_values(by='Frequency', ascending=False)

print("Activity Analysis During Normal Periods:")
print(activity_analysis_n)

# Group by Case - Anomalous Periods
case_analysis = anomalous_log.groupby('case:concept:name').agg(
    TotalDuration=('Timestamp', lambda x: (x.max() - x.min()).total_seconds() / 3600),
    ActivityCount=('concept:name', 'count')
).sort_values(by='TotalDuration', ascending=False)

print("Case Analysis During Anomalous Periods:")
print(case_analysis.head())

# Group by Case - Normal Periods
case_analysis_n = normal_periods.groupby('case:concept:name').agg(
    TotalDuration=('Timestamp', lambda x: (x.max() - x.min()).total_seconds() / 3600),
    ActivityCount=('concept:name', 'count')
).sort_values(by='TotalDuration', ascending=False)

print("Case Analysis During Normal Periods:")
print(case_analysis_n.head())

# ............................................................

# VISUALIZATION - Throughput Time and Rate of Change (ROC)

fig, ax1 = plt.subplots(figsize=(14, 8))

ax1.set_xlabel('Date')
ax1.set_ylabel('Average Throughput Time (hours)', color='blue')
ax1.plot(daily_throughput['Date'], daily_throughput['AverageThroughputTime'], label='Avg Throughput Time', color='blue', marker='o')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.tick_params(axis='x', rotation=45)

ax2 = ax1.twinx()
ax2.set_ylabel('ROC (hours/day)', color='red')
ax2.plot(daily_throughput['Date'], daily_throughput['ROC'], label='ROC', color='red', linestyle='--', marker='x')
ax2.tick_params(axis='y', labelcolor='red')

ax1.xaxis.set_major_locator(mdates.MonthLocator()) 
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.title('Average Throughput Time and Rate of Change (ROC)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax1.grid(True)
fig.tight_layout()
plt.show()

# ............................................................