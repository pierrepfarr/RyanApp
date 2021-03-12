from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import string

letters = list(string.ascii_lowercase)
url_base = "https://www.basketball-reference.com/players/"

output_folder = "/Users/pierre/Desktop/RyanApp/"

for letter in letters:

    output_file = 'players_'+letter+'.csv'

    url = url_base + letter +'/'
    html = urlopen(url)
    soup = BeautifulSoup(html)

    soup.findAll('tr', limit=2)

    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

    rows = soup.findAll('tr')[1:]

    player_names = [[td.getText() for td in rows[i].findAll('th')]
                for i in range(len(rows))]

    player_info = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]

    name = pd.DataFrame(player_names, columns = [headers[0]])
    info = pd.DataFrame(player_info, columns = headers[1:])

    players = pd.concat([name,info],axis=1)
    players.to_csv(output_file)