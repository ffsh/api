#!/usr/bin/python3
""" API Updater for Freifunk JSON files """
import json
import datetime
import argparse
import requests
import sys
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class API():
    """ API Updater class for Freifunk JSON files """
    def __init__(self, filename, meshviewer_url):
        super().__init__()
        self.filename = filename
        self.meshviewer_url = meshviewer_url
        retry_strategy = Retry(
            total=10,
            backoff_factor=2,
            status_forcelist=(429, 500, 502, 503, 504),
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

        response = self.http.get(self.meshviewer_url, timeout=30)
        response.raise_for_status()
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
        api_data["state"]["lastchange"] = datetime.datetime.now(
            datetime.timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        with open(self.filename, "w") as api_file:
            json.dump(api_data, api_file, indent=2)
        print("updated your file")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-filename", help="filename", required=True)
    parser.add_argument("-url", help="url", required=True)
    args = parser.parse_args()

    api = API(args.filename, args.url)
    try:
        api.validate()
    except (OSError, json.JSONDecodeError) as error:
        print("Could not read JSON file: {}".format(error))
        return 1
    try:
        api.update_nodes()
    except requests.exceptions.RequestException as error:
        print("Network request failed: {}".format(error))
        return 1
    return 0
    

if __name__ == '__main__':
    sys.exit(main())
