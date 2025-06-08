import os
import glob
import pandas as pd
import tqdm

PATH_TO_DATASETS = "Datasets/"
data_folder = f"{PATH_TO_DATASETS}AirPollutionDatasets/"
csv_files = glob.glob(data_folder + "*.csv")

def melt_wide_airpollution_csv(file):
    headers = pd.read_csv(file, sep=';', nrows=3, header=None)
    df = pd.read_csv(file, sep=';', skiprows=3, header=None, dtype=str)
    sensors = headers.iloc[0].tolist()
    fields = headers.iloc[1].tolist()
    units = headers.iloc[2].tolist()
    columns = []
    for i, (sensor, field, unit) in enumerate(zip(sensors, fields, units)):
        columns.append((str(sensor).strip(';').replace('"',''), str(field).strip(';').replace('"',''), str(unit).strip(';').replace('"','')))
    df.columns = pd.MultiIndex.from_tuples(columns)
    sensor_names = [c[0] for c in df.columns if c[0] and c[0] != '']
    sensor_names = sorted(set(sensor_names))
    melted_rows = []
    for sensor in sensor_names:
        cols = [c for c in df.columns if c[0] == sensor]
        if not cols:
            continue
        subdf = df[cols].copy()
        subdf.columns = [c[1] for c in cols]
        subdf['Sensor'] = sensor
        subdf['Time_UTC'] = df[('','','')].iloc[:,0] if ('','','') in df.columns else df.iloc[:,0]
        subdf['Time_Local'] = df[('','','')].iloc[:,1] if ('','','') in df.columns else df.iloc[:,1]
        melted_rows.append(subdf)
    for i, subdf in enumerate(melted_rows):
        subdf = subdf.loc[:, ~subdf.columns.duplicated()]
        melted_rows[i] = subdf
    melted = pd.concat(melted_rows, ignore_index=True)
    melted = melted.loc[:,~melted.columns.duplicated()]
    cols_order = ['Sensor', 'Time_UTC', 'Time_Local', 'Lat', 'Lon', 'PM1', 'PM2.5', 'PM10', 'NO2']
    cols_present = [c for c in cols_order if c in melted.columns]
    melted = melted[cols_present]
    return melted

df_list = []
sensor_locations = {}

for file in tqdm.tqdm(csv_files, desc="Merging CSV files", unit="file"):
    melted = melt_wide_airpollution_csv(file)
    df_list.append(melted)
    # Extract sensor locations
    for sensor in melted['Sensor'].unique():
        sub = melted[melted['Sensor'] == sensor]
        lat = sub['Lat'].dropna().iloc[0] if 'Lat' in sub and not sub['Lat'].dropna().empty else None
        lon = sub['Lon'].dropna().iloc[0] if 'Lon' in sub and not sub['Lon'].dropna().empty else None
        if sensor not in sensor_locations and lat and lon:
            sensor_locations[sensor] = {'Sensor': sensor, 'Lat': lat, 'Lon': lon}

merged_df = pd.concat(df_list, ignore_index=True)

abs_path = os.path.abspath(PATH_TO_DATASETS)
print(f"Saving merged data to {abs_path}")

output_file = os.path.join(PATH_TO_DATASETS, 'merged_air_pollution_data.csv')
merged_df.to_csv(output_file, index=False)

# Save sensor locations
locations_df = pd.DataFrame(list(sensor_locations.values()))
locations_file = os.path.join(PATH_TO_DATASETS, 'air_pollution_sensor_locations.csv')
locations_df.to_csv(locations_file, index=False)

print("DONE")