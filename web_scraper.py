from bs4 import BeautifulSoup
import urllib
def cool():
    r = urllib.urlopen('https://www.service.transport.qld.gov.au/checkrego/application/VehicleResult.xhtml?windowId=de9').read()
    print r

cool()


#if __name__ == '__main__':
 #   cool()
