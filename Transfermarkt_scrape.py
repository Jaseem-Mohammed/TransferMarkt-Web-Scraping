from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd



name = []
position = []
rank = []
age = []
country = []
club = []
value = []
for i in range(1,21):
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = f"https://www.transfermarkt.co.uk/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page={i}"
    print(f'scraping page {i} of 20...')
    response = requests.get(page, headers=headers)
    print(f'status code: {response.status_code}')
    soup = BeautifulSoup(response.content, 'html.parser')
    d = soup.find(class_='responsive-table').find('tbody').select('.odd, .even')
    for p in d:
        name.append(p.table.find(class_='hauptlink').find('a').get_text())
        position.append(p.table.find_all('tr')[1].get_text())
        rank.append(p.find(class_='zentriert').get_text())
        age.append(p.select('td.zentriert')[1].get_text())
        country.append(p.select('td.zentriert')[2].find('img')['title'])
        club.append(p.select('td.zentriert')[3].find('a').find('img')['alt'])
        value.append(p.find_all(class_='hauptlink')[1].get_text())
    sleep(3)


df = pd.DataFrame({
    'Rank': rank,
    'Name': name,
    'Age': age,
    'Position': position,
    'Country': country,
    'club': club,
    'Value': value})

df.to_csv('Most_Valuable_players_8-20.csv', index=False)
print(df.info())