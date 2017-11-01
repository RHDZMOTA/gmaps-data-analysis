
import googlemaps
import numpy as np
import pandas as pd

from conf.settings import SNAP_TO_ROAD_KEY


def row_to_df(row):
    return pd.DataFrame({
        "lat": eval(row.lat.replace("\n", "").replace(" ", ",").replace(",,", ",").replace("[,", "[")),
        "lng": eval(row.lng.replace("\n", "").replace(" ", ",").replace(",,", ",").replace("[,", "["))}
    )


class TripEnhancer(object):

    def __init__(self, api_key):
        self.key = api_key
        self.gmaps = googlemaps.Client(key=self.key)

    @staticmethod
    def df_to_string(df):
        def build_string(df, result='points='):
            length = len(df)
            if length == 0:
                return result
            val = df.iloc[0]
            result = result + (result != 'points=') * '|' + str(val["lat"]) + ',' + str(val["lng"])
            result = build_string(df[1:], result=result)
            return result
        return build_string(df)

    @staticmethod
    def snapdata_to_df(snap_data):
        lat, lng = [], []
        for i in range(len(snap_data)):
            lat.append(snap_data[i]['location']['latitude'])
            lng.append(snap_data[i]['location']['longitude'])
        return pd.DataFrame({'lat': lat, 'lng': lng})

    def snap_road(self, data):
        data_as_string = self.df_to_string(data).split('=')[-1]
        snap_data = self.gmaps.snap_to_roads(interpolate=True, path=data_as_string)
        return self.snapdata_to_df(snap_data)

