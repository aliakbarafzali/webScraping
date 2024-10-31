import requests
import csv
import os
import json
from bs4 import BeautifulSoup

def getPage(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def getPlayerRows(page):
    table = page.find("table", class_="items") if page else None
    tbody = table.find("tbody") if table else None
    return tbody.find_all("tr") if tbody else []

def getPlayers(rows):
    players = {}
    for player in rows:
        posrela = player.find("td", class_="posrela")
        market_value = player.find("td", class_="rechts hauptlink")
        age_cell, nationality_cell = None, None
        found_age = False

        for cell in player.find_all("td", class_="zentriert"):
            if "rueckennummer" not in cell.get("class", []):
                if not found_age:
                    age_cell = cell
                    found_age = True
                else:
                    nationality_cell = cell
                    break

        if posrela and age_cell and market_value:
            inline_table = posrela.find("table", class_="inline-table")
            if inline_table:
                name = inline_table.find_all("tr")[0].find("td", class_="hauptlink").a.text.strip()
                position = inline_table.find_all("tr")[1].td.text.strip()
                age = age_cell.text.strip()
                nationalities = " / ".join([img["alt"] for img in nationality_cell.find_all("img", alt=True)])
                players[name] = {
                    "position": position,
                    "age": age,
                    "nationality": nationalities,
                    "value": market_value.text.strip()
                }

    return players

def pretty_print(players_data):
    print("Players Information:\n" + "="*50)
    for name, info in players_data.items():
        print(f"Name: {name}")
        print(f"  Position: {info['position']}")
        print(f"  Age: {info['age']}")
        print(f"  Nationality: {info['nationality']}")
        print(f"  Market Value: {info['value']}")
        print("-" * 50)

def print_team_names(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        
        if "teams" not in data or not isinstance(data["teams"], list):
            print("Invalid JSON format.")
            return []
        
        print("\nLa Liga Teams:")
        for index, team in enumerate(data["teams"], start=1):
            print(f"{index}. {team['name']}")
        
        return data["teams"]
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading the JSON file: {e}")
        return []

def export_csv(players_data, filename="players.csv"):
    if not players_data:
        print("No player data available to export.")
        return

    os.makedirs("generated_csv", exist_ok=True)
    filepath = os.path.join("generated_csv", filename)

    try:
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Position", "Age", "Nationality", "Market Value"])
            for name, info in players_data.items():
                writer.writerow([name, info['position'], info['age'], info['nationality'], info['value']])
        print(f"Players data successfully exported to {filepath}")
    
    except Exception as e:
        print(f"An error occurred while exporting to CSV: {e}")

def main():
    teams = print_team_names("urls.json")
    if not teams:
        return

    try:
        choice = int(input("\nChoose a team by entering its number: "))
        if choice < 1 or choice > len(teams):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    selected_team = teams[choice - 1]["name"]
    print(f"\nYou selected: {selected_team}")

    action = input("Do you want to (P)retty print the players or (E)xport to CSV? ").strip().lower()

    page = getPage(teams[choice - 1]["custom_url"])
    rows = getPlayerRows(page)
    players_data = getPlayers(rows)

    if action == "p":
        pretty_print(players_data)
    elif action == "e":
        csv_filename = f"{selected_team.replace(' ', '_').lower()}_players.csv"
        export_csv(players_data, csv_filename)
    else:
        print("Invalid action selected.")

if __name__ == "__main__":
    main()
