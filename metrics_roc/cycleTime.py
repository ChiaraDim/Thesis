import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -------------------------------------------------------
#                      CYCLE TIME
# -------------------------------------------------------

log_file = "logs/orders_log.csv"
event_log = pd.read_csv(log_file)

event_log['Timestamp'] = pd.to_datetime(event_log['time:timestamp'], errors='coerce')

start_end_timestamps = (event_log.groupby('case:concept:name')['Timestamp']
                        .agg(StartTimestamp='min', EndTimestamp='max')
                        .reset_index())

start_end_timestamps['CycleTime (hours)'] = (
    (start_end_timestamps['EndTimestamp'] - start_end_timestamps['StartTimestamp'])
    .dt.total_seconds() / 3600
)

start_end_timestamps['Date'] = start_end_timestamps['StartTimestamp'].dt.date
daily_metrics = (start_end_timestamps.groupby('Date')['CycleTime (hours)']
                 .mean()
                 .reset_index(name='AverageCycleTime'))

daily_metrics['ROC'] = daily_metrics['AverageCycleTime'].diff()/1

# ............................................................

# Define anomalous periods
anomalous_periods = [
    ('2023-05-01 00:00:00+00:00', '2023-06-30 23:59:59+00:00'),
    ('2023-08-01 00:00:00+00:00', '2023-09-30 23:59:59+00:00'),
    ('2023-09-01 00:00:00+00:00', '2023-10-31 23:59:59+00:00'),
    ('2024-03-01 00:00:00+00:00', '2024-04-30 23:59:59+00:00')
]

filtered_logs = []
for start, end in anomalous_periods:
    filtered_logs.append(event_log[(event_log['Timestamp'] >= pd.Timestamp(start)) &
                                   (event_log['Timestamp'] <= pd.Timestamp(end))])
anomalous_log = pd.concat(filtered_logs)

print("Filtered Event Log for Anomalous Periods:")
print(anomalous_log.head())

# ............................................................

# Group by Activity
activity_analysis = anomalous_log.groupby('concept:name').agg(
    TotalDuration=('Timestamp', lambda x: (x.max() - x.min()).total_seconds() / 3600),
    Frequency=('concept:name', 'count')
).sort_values(by='Frequency', ascending=False)

print("Activity Analysis During Anomalous Periods:")
print(activity_analysis)

# Group by Case
case_analysis = anomalous_log.groupby('case:concept:name').agg(
    TotalDuration=('Timestamp', lambda x: (x.max() - x.min()).total_seconds() / 3600),
    ActivityCount=('concept:name', 'count')
).sort_values(by='TotalDuration', ascending=False)

print("Case Analysis During Anomalous Periods:")
print(case_analysis.head())

# ............................................................

# VISUALIZATION - Cycle Time and Rate of Change (ROC)

fig, ax1 = plt.subplots(figsize=(14, 8))

ax1.set_xlabel('Date')
ax1.set_ylabel('Average Cycle Time (hours)', color='blue')
ax1.plot(daily_metrics['Date'], daily_metrics['AverageCycleTime'], label='Avg Cycle Time', color='blue', marker='o')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.tick_params(axis='x', rotation=45)

ax2 = ax1.twinx()
ax2.set_ylabel('ROC (hours/day)', color='red')
ax2.plot(daily_metrics['Date'], daily_metrics['ROC'], label='ROC', color='red', linestyle='--', marker='x')
ax2.tick_params(axis='y', labelcolor='red')

ax1.xaxis.set_major_locator(mdates.MonthLocator())  
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.title('Average Cycle Time and Rate of Change (ROC)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax1.grid(True)
fig.tight_layout()
plt.show()

# ............................................................