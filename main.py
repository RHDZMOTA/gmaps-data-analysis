import numpy as np
import pandas as pd
import datetime as dt


from util.data_operations import get_dataset
from util.distance_operations import harversine, distance_df
from util.trip_enhancement import TripEnhancer, SNAP_TO_ROAD_KEY
from conf.settings import FilesConfig


TRIP_DEFINITON = 7 * 60 * 1000
TRIP_RELEVANCE = 2017 + 10/12
SAVE = True


def create_table(save=False):
    df = get_dataset()
    df["timestamp"] = df.timestamp.astype(int).values
    df = df.sort_values("timestamp")
    if save:
        df.to_csv(FilesConfig.FileNames.datapoints_csv, index=False)
    return df


def create_trips(df, save=False):
    trip_enhancer = TripEnhancer(SNAP_TO_ROAD_KEY)
    driving_df = df.query("likely_activity == 'IN_VEHICLE'").copy()
    driving_df["delta_time"] = [0] + list(driving_df.timestamp.values[1:] - driving_df.timestamp.values[:-1])
    driving_df["trip_id"] = np.cumsum(driving_df.delta_time.values > TRIP_DEFINITON)
    trips = pd.DataFrame([], columns=["id", "distance", "time", "lat", "lng"])
    ids, distance, time, lats, lngs = [], [], [], [], []
    enhanced_lats, enhanced_lngs = [], []
    initial_unix_time, initial_date_time = [], []
    deleted_trips = 0
    for trip in driving_df.trip_id.unique():
        trip_data = driving_df.query("trip_id == {}".format(trip))
        if len(trip_data) < 5:
            deleted_trips += 1
            continue
        distance.append(distance_df(trip_data).apply(harversine, 1).sum())
        time.append(trip_data.timestamp.values[-1] - trip_data.timestamp.values[0])
        initial_unix_time.append(trip_data.timestamp.values[0])
        temp_time = int(trip_data.timestamp.values[0]/1000)
        initial_date_time.append(dt.datetime.fromtimestamp(temp_time))
        ids.append(trip)
        lats.append(trip_data.lat.values)
        lngs.append(trip_data.lng.values)
        if dt.datetime.fromtimestamp(temp_time).year + dt.datetime.fromtimestamp(temp_time).month > TRIP_RELEVANCE:
            try:
                temp = trip_enhancer.snap_road(pd.DataFrame({"lat": trip_data.lat.values, "lng": trip_data.lng.values}))
                enhanced_lats.append(list(temp.lat.values))
                enhanced_lngs.append(list(temp.lng.values))
            except Exception as e:
                enhanced_lats.append([])
                enhanced_lngs.append([])
        else:
            enhanced_lats.append([])
            enhanced_lngs.append([])
    trips["id"] = ids
    trips["distance"] = distance
    trips["start_unix_time"] = initial_unix_time
    trips["start_date_time"] = initial_date_time 
    trips["time"] = time
    trips["lat"] = lats
    trips["enhanced_lats"] = enhanced_lats
    trips["lng"] = lngs
    trips["enhanced_lngs"] = enhanced_lngs
    trips["n_datapoints"] = trips.apply(lambda x: len(x["lat"]), 1).values
    if save:
        trips.to_csv(FilesConfig.FileNames.trips_csv, index=False)
    return trips


def main():
    df = create_table(SAVE)
    trips = create_trips(df, SAVE)



if __name__ == "__main__":
    main()
