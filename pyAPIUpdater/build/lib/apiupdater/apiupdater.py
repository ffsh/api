#!/usr/bin/python3
""" mediamanger """
import os
import json
import datetime
import argparse
import requests
import sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib3.exceptions import MaxRetryError

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
        retry_strategy = Retry(
            total=10,
            backoff_factor=2
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.http = requests.Session()
        self.http.mount("https://", adapter)
        self.http.mount("http://", adapter)

    def validate(self):
        with open(self.filename) as api_file:
            json.load(api_file)

    def update_nodes(self):
        # Get the current json file

        response = self.http.get(self.meshviewer_url)
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
    try:
        api.validate()
    except Exception as e:
        print("Exception opening the file: {}".format(e))
        sys.exit(1)
    try:
        api.update_nodes()
    except MaxRetryError:
        print("Network unreachable")
    

if __name__ == '__main__':
    main()
