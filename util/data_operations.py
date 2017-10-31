import pandas as pd
import numpy as np
import json

from conf.settings import FilesConfig


def get_gmaps_data():
    with open(FilesConfig.FileNames.gmaps_data, "rb") as file:
        json_data = json.load(file)
    return json_data


def get_dataset():
    json_data = get_gmaps_data()
    activities = ["IN_VEHICLE", "ON_BICYCLE", "ON_FOOT", "RUNNING", "STILL", "TILTING", "UNKNOWN", "WALKING"]
    rows = []
    for element in json_data['locations']:
        row = {
            "accuracy": element.get("accuracy"),
            "alt": element.get("altitude"),
            "lat": element.get("latitudeE7") / 10 ** 7,
            "lng": element.get("longitudeE7") / 10 ** 7,
            "timestamp": element.get("timestampMs"),
            "EXITING_VEHICLE": 0,
            "IN_VEHICLE": 0,
            "ON_BICYCLE": 0,
            "ON_FOOT": 0,
            "RUNNING": 0,
            "STILL": 0,
            "TILTING": 0,
            "UNKNOWN": 0,
            "WALKING": 0,
            "likely_activity": "UNKNOWN"
        }
        if not element.get("activity"):
            continue
        for activity in element["activity"]:
            if not activity.get("activity"):
                continue
            for act in activity["activity"]:
                if not act.get("type"):
                    continue
                row[act.get("type")] = act.get("confidence")
            confidence = [row.get(act_name) for act_name in activities]
            if sum(confidence) > 5:
                row["likely_activity"] = activities[np.argmax(confidence)]
            rows.append(row)

    return pd.DataFrame(rows)

