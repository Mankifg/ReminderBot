import json


def read():
    with open('./data/schedule.json', 'r') as f:
        data = json.load(f)
        return data


def write(data):
    with open('./data/schedule.json', 'w') as f:
        json.dump(data, f)
