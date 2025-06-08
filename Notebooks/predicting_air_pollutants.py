import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics.pairwise import haversine_distances
from sklearn.preprocessing import LabelEncoder

DATASETS_PATH = "Datasets/"

sensors_df = pd.read_csv(DATASETS_PATH + "merged_air_pollution_data_clean.csv")

neighborhoods_df = pd.read_csv(DATASETS_PATH + "/Raw Datasets/buurten.csv", delimiter=';')

known_neighs = sensors_df['Neighbourhood'].unique()
missing_neighs_df = neighborhoods_df[~neighborhoods_df['BUURTNAAM'].isin(known_neighs)]

agg_cols = [col for col in sensors_df.columns if 'mean' in col]
yearly_avg_df = sensors_df.groupby('Neighbourhood')[agg_cols + ['LAT', 'LON']].mean().reset_index()

def idw_predict(lat, lon, known_df, feature, power=2):
    coords = np.radians(known_df[['LAT', 'LON']].values)
    target_coord = np.radians([[lat, lon]])
    dists = haversine_distances(target_coord, coords)[0] * 6371000  
    dists[dists == 0] = 0.001 
    weights = 1 / (dists ** power)
    values = known_df[feature].values
    return np.sum(weights * values) / np.sum(weights)

idw_predictions = []
for _, row in missing_neighs_df.iterrows():
    preds = {'Neighbourhood': row['BUURTNAAM'], 'LAT': row['geo_point_2d'].split(',')[0], 'LON': row['geo_point_2d'].split(',')[1]}
    lat = float(preds['LAT'])
    lon = float(preds['LON'])
    for col in agg_cols:
        preds[f'{col}_idw'] = idw_predict(lat, lon, yearly_avg_df, col)
    idw_predictions.append(preds)

idw_df = pd.DataFrame(idw_predictions)

rf_predictions = []
for col in agg_cols:
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    X = yearly_avg_df[['LAT', 'LON']]
    y = yearly_avg_df[col]
    rf.fit(X, y)
    pred = rf.predict(idw_df[['LAT', 'LON']].astype(float))
    idw_df[f'{col}_rf'] = pred

for col in agg_cols:
    idw_col = f'{col}_idw'
    rf_col = f'{col}_rf'
    idw_df[f'{col}_hybrid'] = (idw_df[idw_col] + idw_df[rf_col]) / 2

pollutant_map = {f'{col}_hybrid': col for col in agg_cols}
hybrid_df = idw_df[['Neighbourhood', 'LAT', 'LON'] + list(pollutant_map.keys())]
hybrid_df.rename(columns=pollutant_map, inplace=True)

original_df = yearly_avg_df[['Neighbourhood', 'LAT', 'LON'] + agg_cols]

combined_df = pd.concat([original_df, hybrid_df], ignore_index=True)

combined_df.to_csv(DATASETS_PATH + "predicted_air_pollution.csv", index=False)