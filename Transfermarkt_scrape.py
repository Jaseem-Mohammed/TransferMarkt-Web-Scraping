
from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd

#the different data & values will be added to these lists.
name = []
position = []
rank = []
age = []
country = []
club = []
value = []

#there are total 20 pages of data which we need in this case, hence we take i in range(21).
for i in range(1,21):
    #without the 'header' parameter the code seems to be not working!
    headers = {'User-Agent': 'tmscraper_v_1'}
    page = f"https://www.transfermarkt.co.uk/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page={i}"
    print(f'scraping page {i} of 20...')
    
    response = requests.get(page, headers=headers)
    print(f'status code of page {i}: {response.status_code}')
    
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find(class_='responsive-table').find('tbody').select('.odd, .even')
    
    #appending all the different aspects of a player to appropriate lists.
    for p in data:
        name.append(p.table.find(class_='hauptlink').find('a').get_text())
        position.append(p.table.find_all('tr')[1].get_text())
        rank.append(p.find(class_='zentriert').get_text())
        age.append(p.select('td.zentriert')[1].get_text())
        country.append(p.select('td.zentriert')[2].find('img')['title'])
        club.append(p.select('td.zentriert')[3].find('a').find('img')['alt'])
        value.append(p.find_all(class_='hauptlink')[1].get_text())
    sleep(3)
#Turning & combining the lists into a dataframe.
df = pd.DataFrame({
    'Rank': rank,
    'Name': name,
    'Age': age,
    'Position': position,
    'Country': country,
    'club': club,
    'Value': value})

#Saving the dataframe as a csv file.
df.to_csv('Most_Valuable_players_8-20.csv', index=False)
print(df.info())
