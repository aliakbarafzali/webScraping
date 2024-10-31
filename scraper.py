import requests, re
from bs4 import BeautifulSoup

def getPage(): # Etabli la connection
    URL = "https://www.transfermarkt.com/real-madrid/startseite/verein/418"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        page = requests.get(URL, headers=headers)
    except:
        print("Error")
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def getPlayerRows(page):  # Parcourt toutes les lignes du tbody
    table = page.find("table", class_="items")  # Trouve la table avec la classe 'items'
    tbody = table.find("tbody")  # Sélectionne le tbody

    rows = tbody.find_all("tr")  # Trouve toutes les lignes du tbody
    return rows

def getPlayers(rows): # Retourne une hash de players
    players_hash = {}
    for player in rows:

        posrela_cell = player.find("td", class_="posrela")
        # Find the first `zentriert` cell that does not contain `rueckennummer`
        age_cell = None
        for td in player.find_all("td", class_="zentriert"):
            if "rueckennummer" not in td.get("class", []):
                age_cell = td
                break
        
        nationality_cell = player.find_all("td", class_="zentriert")[2]

        if posrela_cell and age_cell:
            inline_table = posrela_cell.find("table", class_="inline-table")
            if inline_table:
                # Extract player name from the first row's 'hauptlink' class
                name_row = inline_table.find_all("tr")[0]
                playerName = name_row.find("td", class_="hauptlink").find("a").text.strip()

                # Extract position from the second row
                position_row = inline_table.find_all("tr")[1]
                position = position_row.find("td").text.strip()

                # Extract age from age_cell
                age = age_cell.text.strip()
                
                 # Extract nationalities from nationality_cell
                nationalities = [
                    img["alt"] for img in nationality_cell.find_all("img", alt=True)
                ]
                nationality = " / ".join(nationalities)  # Concatenate with '/

                # Store player data in players_hash
                players_hash[playerName] = {
                    "value": 0,     # Placeholder for value
                    "age": age,     # Extracted age
                    "position": position,
                    "nationality": nationality
                }

    return players_hash

        

page = getPage()
rows = getPlayerRows(page)
players = getPlayers(rows)
print(players['Ferland Mendy']["age"])


