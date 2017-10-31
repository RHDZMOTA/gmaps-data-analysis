import numpy as np
import pandas as pd


def degree_to_radian(degree):
    return 2 * degree * np.pi / 360


def harversine(x):
    initial_coord, final_coord = x[["initial_lat", "initial_lng"]].values, x[["final_lat", "final_lng"]].values
    r = 6371
    initial_rads = list(map(degree_to_radian, initial_coord))
    final_rads = list(map(degree_to_radian, final_coord))
    delta_phi = final_rads[0] - initial_rads[0]
    delta_lambda = initial_rads[1] - final_rads[1]
    h = np.power(np.sin(delta_phi/2), 2) + \
        np.cos(initial_rads[0]) * np.cos(final_rads[0]) * \
        np.power(np.sin(delta_lambda/2), 2)
    return 2*r*np.arcsin(np.sqrt(h))


def distance_df(trip_data):
    temp = pd.concat([
        trip_data[["lat", "lng"]][1:].reset_index(drop=True),
        trip_data[["lat", "lng"]][:-1].reset_index(drop=True)],
        1)
    temp.columns = ["initial_lat", "initial_lng", "final_lat", "final_lng"]
    return temp