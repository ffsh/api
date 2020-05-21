#!/usr/bin/python3
""" mediamanger """
import os
import json
import datetime
import argparse
import requests

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-filename", help="filename", required=True)
PARSER.add_argument("-url", help="url", required=True)


ARGS = PARSER.parse_args()

class API():
    """ thats a MediaManager """
    def __init__(self, filename, meshviewer_url):
        super().__init__()
        self.filename = filename
        self.meshviewer_url = meshviewer_url

    def validate(self):
        with open(self.filename) as api_file:
            json.load(api_file)

    def update_nodes(self):
        # Get the current json file
        response = requests.get(self.meshviewer_url)
        data = response.json()
        node_counter = 0
        for node in data["nodes"]:
            if node["is_online"]:
                node_counter += 1
        print("Found {} online Nodes".format(node_counter))
        api_data = None

        with open(self.filename) as api_file:
            api_data = json.load(api_file)

        print("File loaded")

        api_data["state"]["nodes"] = node_counter
        api_data["state"]["lastchange"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        with open(self.filename, "w") as api_file:
            json.dump(api_data, api_file, indent=2)
        print("updated your file")

def main():
    api = API(ARGS.filename, ARGS.url)
    api.validate()
    api.update_nodes()

if __name__ == '__main__':
    main()
