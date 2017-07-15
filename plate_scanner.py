import json
import os

import time
from openalpr import Alpr
from selenium import webdriver
from web_scraper import read_page


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
    open(filename, "w").write(json.dumps(data))
    return data


def get_page(rego):
    driver = webdriver.Chrome()
    driver.get("https://www.service.transport.qld.gov.au/checkrego/"
               "application/TermAndConditions.xhtml?windowId=9b2")
    driver.find_element_by_id("tAndCForm:confirmButton").click()
    driver.find_element_by_id("vehicleSearchForm:plateNumber").send_keys(rego)
    driver.find_element_by_id("vehicleSearchForm:confirmButton").click()
    src = driver.page_source
    driver.close()
    return src


if __name__ == '__main__':
    if not os.path.exists("cache"):
        os.makedirs("cache")

    alpr = Alpr("au", "openalpr.conf", "")
    alpr.set_top_n(50)
    alpr.set_default_region("qld")

    for filename in os.listdir("Car photos"):
        run("Car photos/" + filename)
