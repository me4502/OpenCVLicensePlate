from bs4 import BeautifulSoup


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
