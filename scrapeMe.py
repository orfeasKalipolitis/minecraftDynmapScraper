from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
import json

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
    # get that soup
    soup = BS(driver.page_source, 'lxml')
    ul = soup.find_all('ul')
    # ul[4] contains the players currently connected
    #
    # get those players
    players = ul[4].find_all('li')
    #
    # get all that pertinent info
    entry = {}
    entry['numOfPlayers'] = str(len(players))
    entry['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    entry['playerNames'] = []
    for player in players:
        entry['playerNames'].append(player.find(title='Center on player').text)
    #
    # write all of that info down
    with open('ServerStatistics.log', 'a') as outputFile:
        json.dump(entry, outputFile, sort_keys=True, indent=4)
        outputFile.write(',\n')
    print(entry['timestamp'] + ': ' + str(len(players)) + ' players currently online on classic survival.')
    #
    # good job, go to sleep now
    time.sleep(interval)