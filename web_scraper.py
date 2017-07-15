from bs4 import BeautifulSoup
from urllib import urlopen
import re

# create a dictionary
list = []


# specify the url
def read_page(webpage):
    soup = BeautifulSoup(webpage, 'html.parser')
    dl_list = soup.findAll('dl', attrs={'class':'data'})
    for dl in dl_list:
        dd_list = dl.findAll('dd')
        for dd in dd_list:





