import json
import os

import time
from openalpr import Alpr
from web_scraper import read_page, get_page
from googleapiclient.discovery import build

google_api_key = None
cse_token = None


def run(filename):
    results = alpr.recognize_file(filename)

    best_fit = None

    for plate in results['results']:
        for candidate in plate['candidates']:
            best_fit = candidate['plate']
            if candidate['matches_template']:
                break

    if best_fit is not None:
        print "Found License: " + best_fit + " for file: " + filename
        print get_plate_info(best_fit)
    else:
        print "Failed to find a license plate for file: " + filename


def get_plate_info(rego):
    filename = "cache/" + rego + ".json"
    if os.path.exists(filename) \
            and (time.time() - os.path.getmtime(filename) < 60 * 60 * 24):
        return json.loads(open(filename, "r").read())
    data = read_page(get_page(rego))
    if google_api_key is not None:
        service = build("customsearch", "v1", developerKey=google_api_key)
        res = service.cse().list(
            q=data["Vehicle Identification Number (VIN)"],
            cx=cse_token, num=1).execute()
        for request in res["queries"]["request"]:
            if int(request["totalResults"]) == 0:
                data["Resell"] = "Unlikely"
            else:
                data["Resell"] = "Yes"
    open(filename, "w").write(json.dumps(data))
    return data


if __name__ == '__main__':
    if os.path.exists("settings.json"):
        settings_data = json.loads(open("settings.json", "rw").read())
        google_api_key = settings_data['google-api-key']
        cse_token = settings_data['cse-token']

    if not os.path.exists("cache"):
        os.makedirs("cache")

    alpr = Alpr("au", "openalpr.conf", "")
    alpr.set_top_n(50)
    alpr.set_default_region("qld")

    for filename in os.listdir("Car photos"):
        run("Car photos/" + filename)
