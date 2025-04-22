import pandas as pd

def calculate_oee(df, device_id, location, month):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    df_filtered = df[
        (df['Device ID'] == device_id) &
        (df['Location'].str.lower() == location.lower()) &
        (df['Timestamp'].dt.month == month)
    ]

    if df_filtered.empty:
        return None

    planned_time = df_filtered['Planned Time'].sum()
    run_time = df_filtered['Run Time'].sum()
    total_count = df_filtered['Total Count'].sum()
    good_count = df_filtered['Good Count'].sum()

    if planned_time == 0 or run_time == 0 or total_count == 0:
        return 0

    # OEE components
    availability = run_time / planned_time
    ideal_cycle_time = 1.0  # Set to 1 min/unit for simplicity (adjust if needed)
    performance = (ideal_cycle_time * total_count) / run_time
    quality = good_count / total_count

    oee = availability * performance * quality * 100
    return round(oee, 2)
