from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time

# fixing up the url
baseURL = 'http://minecraft.spelenshus.se'
port = '8004'
url = baseURL + ':' + port

# interval to refresh the player stats in seconds
interval = 60 * 60 # Currently set to 1 hour

# get the page
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
driver.get(url)

# parse every hour
while True:
    soup = BS(driver.page_source, 'lxml')
    ul = soup.find_all('ul')
    # ul[4] contains the players currently connected
    players = ul[4].find_all('li')
    print('There are: ' + str(len(players)) + ' players currently connected.')
    time.sleep(interval)