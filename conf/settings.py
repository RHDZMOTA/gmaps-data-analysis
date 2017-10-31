import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATA_FOLDER = os.environ.get("DATA_FOLDER")
RAW_DATA = os.environ.get("RAW_DATA")
MAPS_JSON_DATA = os.environ.get("MAPS_JSON_DATA")
OUTPUT = os.environ.get("OUTPUT")
MAPS_JSON_DATA = os.environ.get("MAPS_JSON_DATA")


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

DATA_PATH = join(PROJECT_DIR, DATA_FOLDER)
RAW_DATA_PATH = join(DATA_PATH, RAW_DATA)
OUTPUT_PATH = join(DATA_PATH, OUTPUT)


class FilesConfig:

    class Paths:
        data = DATA_PATH
        raw_data = RAW_DATA_PATH
        output = OUTPUT_PATH

    class FileNames:
        gmaps_data = join(RAW_DATA_PATH, MAPS_JSON_DATA)
        dataset = join(OUTPUT_PATH, "dataset.csv")


