import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -------------------------------------------------------
#                     SERVICE TIME
# -------------------------------------------------------

log_file = "logs/orders_log.csv"
event_log = pd.read_csv(log_file)

event_log['Timestamp'] = pd.to_datetime(event_log['time:timestamp'], errors='coerce')

activity_service_times = (
    event_log.groupby(['case:concept:name', 'concept:name'])['Timestamp']
    .agg(ActivityStart='min', ActivityEnd='max')
    .reset_index()
)

activity_service_times['ServiceTime (hours)'] = (
    (activity_service_times['ActivityEnd'] - activity_service_times['ActivityStart'])
    .dt.total_seconds() / 3600
)

case_service_times = (
    activity_service_times.groupby('case:concept:name')['ServiceTime (hours)']
    .sum()
    .reset_index()
)

case_start_dates = (
    event_log.groupby('case:concept:name')['Timestamp']
    .min()
    .reset_index()
    .rename(columns={'Timestamp': 'StartTimestamp'})
)

case_service_times = pd.merge(case_service_times, case_start_dates, on='case:concept:name')

case_service_times['Date'] = case_service_times['StartTimestamp'].dt.date

daily_service = (
    case_service_times.groupby('Date')
    .agg(AverageServiceTime=('ServiceTime (hours)', 'mean'),
         CaseCount=('ServiceTime (hours)', 'count'))
    .reset_index()
)

daily_service['ROC'] = daily_service['AverageServiceTime'].diff()

# ............................................................

# Define anomalous periods
anomalous_periods = [
    ('2023-05-01 00:00:00+00:00', '2023-06-30 23:59:59+00:00'),
    ('2023-08-01 00:00:00+00:00', '2023-10-31 23:59:59+00:00'),
    ('2024-03-01 00:00:00+00:00', '2024-04-30 23:59:59+00:00')
]

filtered_anomalous = []
for start, end in anomalous_periods:
    filtered_anomalous.append(event_log[(event_log['Timestamp'] >= pd.Timestamp(start)) &
                                        (event_log['Timestamp'] <= pd.Timestamp(end))])

anomalous_log = pd.concat(filtered_anomalous)

print("Filtered Event Log for Anomalous Periods:")
print(anomalous_log.head())

# ............................................................

# Group by Activity
activity_analysis_anomalous = anomalous_log.groupby('concept:name').agg(
    TotalDuration=('Timestamp', lambda x: (x.max() - x.min()).total_seconds() / 3600),
    Frequency=('concept:name', 'count')
).sort_values(by='Frequency', ascending=False)

print("Activity Analysis During Anomalous Periods:")
print(activity_analysis_anomalous.head())

# Group by Case
case_analysis_anomalous = anomalous_log.groupby('case:concept:name').agg(
    TotalDuration=('Timestamp', lambda x: (x.max() - x.min()).total_seconds() / 3600),
    ActivityCount=('concept:name', 'count')
).sort_values(by='TotalDuration', ascending=False)

print("Case Analysis During Anomalous Periods:")
print(case_analysis_anomalous.head())

# ............................................................

# VISUALIZATION - Service Time and Rate of Change (ROC)

fig, ax1 = plt.subplots(figsize=(14, 8))

ax1.set_xlabel('Date')
ax1.set_ylabel('Average Service Time (hours)', color='blue')
ax1.plot(daily_service['Date'], daily_service['AverageServiceTime'], label='Avg Service Time', color='blue', marker='o')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.tick_params(axis='x', rotation=45)

ax2 = ax1.twinx()
ax2.set_ylabel('ROC (hours/day)', color='red')
ax2.plot(daily_service['Date'], daily_service['ROC'], label='ROC', color='red', linestyle='--', marker='x')
ax2.tick_params(axis='y', labelcolor='red')

ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.title('Average Service Time and Rate of Change (ROC)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax1.grid(True)
fig.tight_layout()
plt.show()
