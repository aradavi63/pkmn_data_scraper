# This file scrapes the images of each Pokemon 
# from various Bulbapedia sources

import os
import requests
from bs4 import BeautifulSoup

# Create the 'img' directory if it doesn't exist
if not os.path.exists('pkmn_icons'):
    os.makedirs('pkmn_icons')

urls = [
    'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number',
    'https://bulbapedia.bulbagarden.net/wiki/Mega_Evolution',
    'https://bulbapedia.bulbagarden.net/wiki/Gigantamax'
]

for url in urls:
    # Get the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all table elements
    tables = soup.findAll('table')

    for table in tables:
        # Find all 'img' tags within each table
        for img in table.findAll('img'):
            if img.get('loading') == 'lazy':
                icon = img.get('src')
                # If the src attribute is relative, add the base URL
                if icon.startswith('http'):
                    img_url = icon
                else:
                    img_url = "https:" + icon
                print(img_url)
                name = img_url.split('/')[-1]
                
                # Check if the image already exists
                file_path = os.path.join('img', name)
                if not os.path.exists(file_path):
                    # Send a request to the image URL
                    img_response = requests.get(img_url)
                    
                    # Write the image content to the file in binary mode
                    with open(file_path, 'wb') as file:
                        file.write(img_response.content)
                else:
                    print(f"Image {name} already exists, skipping download.")

