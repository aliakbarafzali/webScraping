# La Liga Team Scraper

This Python project scrapes detailed player information for selected La Liga teams from Transfrmarket, allowing users to either display player data in the console or export it to a CSV file. This project uses BeautifulSoup for HTML parsing, Requests for web requests, and CSV and JSON libraries for data handling.

## Features

- **Team Selection**: Choose a La Liga team from a pre-defined list in `urls.json`.
- **Data Scraping**: Automatically fetch and parse player details, including:
  - Name
  - Position
  - Age
  - Nationality
  - Market Value
- **Pretty Print**: Display player data in a structured format in the console.
- **CSV Export**: Export player data to a CSV file in a `generated_csv` directory.

## Project Structure

```plaintext
├── generated_csv/       # Directory where exported CSV files are saved
├── urls.json            # JSON file containing La Liga team URLs
├── scraper.py           # Main script with all functions and the main program
└── README.md            # Project documentation
```

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/la-liga-team-scraper.git
   cd la-liga-team-scraper
   ```

2. **Install Dependencies**:
   Make sure you have Python 3.x installed, then install required libraries:
   ```bash
   pip install requests beautifulsoup4
   ```


## Usage

Run the main script:
```bash
python scraper.py
```

1. **Choose a Team**: The program will display a list of La Liga teams. Enter the number corresponding to your team choice.
2. **Select Action**: Choose to either:
   - (P)retty print the data in the console, or
   - (E)xport the data to a CSV file.

The CSV file will be saved in the `generated_csv` directory.

## Code Overview

- **getPage(URL)**: Fetches the HTML content of the team page.
- **getPlayerRows(page)**: Locates the table rows containing player data.
- **getPlayers(rows)**: Extracts player details from each row and structures them in a dictionary.
- **pretty_print(players_data)**: Displays player information in a readable format.
- **print_team_names(filename)**: Lists all available La Liga teams from `urls.json`.
- **export_csv(players_data, filename)**: Saves player data to a CSV file in `generated_csv`.

## Example Output

### Console Output (Pretty Print)

```
Players Information:
==================================================
Name: Luka Modric
  Position: Midfielder
  Age: 35
  Nationality: Croatia
  Market Value: €10M
--------------------------------------------------
...
```

### CSV File Format

The CSV file will have the following columns:
- Name
- Position
- Age
- Nationality
- Market Value

Example row in CSV:
```csv
Name,Position,Age,Nationality,Market Value
Luka Modric,Midfielder,35,Croatia,€10M
```

## Error Handling

- If the URL is unreachable, `getPage` will print an error message.
- Missing data elements (e.g., missing table rows or cells) are handled gracefully, with defaults or informative print statements.

## Contributing

1. Fork the project.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Added feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This README provides a clear guide on setting up, running, and understanding the project. Feel free to modify based on any specific preferences or repository details!
