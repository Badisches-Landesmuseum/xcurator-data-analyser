import json
import logging

import pandas as pd

from resources.resource_manager import ResourceManager

resource_manager = ResourceManager()


def extract_to_csv(col_name, parent_name, json_path_file):
    data = json.load(open(json_path_file))
    records = pd.DataFrame(data[parent_name])
    technik = pd.DataFrame(records[col_name])
    file_path = "resources/" + col_name + ".csv"
    technik.to_csv(file_path)
    print("extracted file to: ", file_path)


if __name__ == "__main__":
    json_path = resource_manager.get('objects/selekt.json')
    extract_to_csv("technik", "records", json_path)
    extract_to_csv("material", "records", json_path)
