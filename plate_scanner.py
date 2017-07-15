import os

from openalpr import Alpr
from selenium import webdriver


def run(file):
    results = alpr.recognize_file(file)

    best_fit = None

    for plate in results['results']:
        for candidate in plate['candidates']:
            best_fit = candidate['plate']
            if candidate['matches_template']:
                break

    if best_fit is not None:
        print "Found License: " + best_fit + " for file: " + file
        #print get_page(best_fit)
    else:
        print "Failed to find a license plate for file: " + file


def get_page(rego):
    driver = webdriver.Chrome()
    driver.get(
        "https://www.service.transport.qld.gov.au/checkrego/application/TermAndConditions.xhtml?windowId=9b2")
    driver.find_element_by_id("tAndCForm:confirmButton").click()
    driver.find_element_by_id("vehicleSearchForm:plateNumber").send_keys(rego)
    driver.find_element_by_id("vehicleSearchForm:confirmButton").click()
    src = driver.page_source
    driver.close()
    return src


if __name__ == '__main__':
    alpr = Alpr("au", "openalpr.conf", "")
    alpr.set_top_n(20)
    alpr.set_default_region("qld")

    for filename in os.listdir("Car photos"):
        run("Car photos/" + filename)
