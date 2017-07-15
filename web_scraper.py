from bs4 import BeautifulSoup
from selenium import webdriver


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


def read_page(webpage):
    soup = BeautifulSoup(webpage, 'html.parser')
    dl_list = soup.findAll('dl', attrs={'class': 'data'})

    page_data = {}

    for dl in dl_list:
        dd_list = dl.findAll('dd')
        dt_list = dl.findAll('dt')
        for index in range(len(dd_list)):
            page_data[dt_list[index].text.strip()] = dd_list[index].text.strip()

    return page_data
