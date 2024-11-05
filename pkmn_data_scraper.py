# This file scrapes the data (name and type) of each Pokemon from Bulbapedia
# Megas and Gmaxes I did manually because I couldn't be bothered as I would need 
# to create a whole new section for them

import requests
from bs4 import BeautifulSoup
import json

# Find natdex info first
natdex_url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'

response = requests.get(natdex_url)
response.raise_for_status()  

soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table')

data = []
row_num = None

# Function to format the name correctly
def format_name(name):
    forms = {"Alolan Form": "-Alola", "Galarian Form": "-Galar", "Hisuian Form": "-Hisui", "Paldean Form": "-Paldea"}
    for form, suffix in forms.items():
        name = name.replace(form, suffix)
    return name

for table in tables:
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) >= 3:
            number = columns[0].get_text(strip=True) or row_num
            name_col_index = 2 if columns[0].get_text(strip=True) else 1
            type_col_index = name_col_index + 1
            name = columns[name_col_index].get_text(strip=True)
            type1 = columns[type_col_index].get_text(strip=True)
            type2 = columns[type_col_index + 1].get_text(strip=True) if len(columns) > type_col_index + 1 else None
            types = f"{type1}, {type2}" if type2 else type1
            row_num = number

            formatted_name = format_name(name)
            data.append([f"{number}; {formatted_name}; {types}"])

json_data = json.dumps(data, indent=4)

print(json_data)

with open('pkmn_data.json', 'w') as f:
    f.write(json_data)


