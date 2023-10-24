import os
import json
import config as config
import pandas as pd
import json

# Function to read the JSON file


def read_dict():
    path = os.path.join(config.CSV_PATH, "filter_dict.json")
    with open(path, 'r') as file:
        data = json.load(file)
        return data


def write_json_file(data):
    path = os.path.join(config.CSV_PATH, "filter_dict.json")
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


def deleteFilter(name_filter):
    dict_filter = read_dict()
    if name_filter not in dict_filter.keys():
        print("Error: Filter", name_filter, "does not exist")
        return
    del dict_filter[name_filter]
    write_json_file(dict_filter)


def getFilter(name_filter):
    dict_filter = read_dict()
    if name_filter not in dict_filter.keys():
        print("Error: Filter", name_filter, "does not exist")
        return
    return dict_filter[name_filter]


def addFilter(df, name_filter):
    dict_filter = read_dict()
    if name_filter in dict_filter.keys():
        print("Error: Filter", name_filter, "already exists")
        return
    dict_filter[name_filter] = df['name'].tolist()
    write_json_file(dict_filter)


def restartFilter(path_folder):
    dict_filter = {}
    dict_filter['all'] = os.listdir(path_folder)
    write_json_file(dict_filter)
