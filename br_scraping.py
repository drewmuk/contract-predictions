import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scraping the data for per-game statistics from Basketball-Reference for a given season
def scrape_basketball_reference_per_game(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page: Status code {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table_id = 'per_game_stats'  
    table = soup.find('table', id=table_id)
    
    if not table:
        print(f"Could not find table with id '{table_id}' on the page")
        return None
    
    data = []
    
    headers = []
    header_row = table.select_one('thead tr')
    if header_row:
        headers = [th.get('data-stat', th.text.strip()) for th in header_row.select('th')]
    
    rows = table.select('tbody tr')
    for row in rows:
        # Skip header rows that can be inserted in the tbody
        if 'class' in row.attrs and 'thead' in row['class']:
            continue
            
        row_data = {}
        cells = row.select('td, th')
        
        for cell in cells:
            # BR uses data-stat for column identification
            stat_name = cell.get('data-stat')
            if stat_name:
                row_data[stat_name] = cell.text.strip()
        
        if row_data:
            data.append(row_data)
    
    df = pd.DataFrame(data)
    return df

# Scraping the data for advanced statistics from Basketball-Reference for a given season
def scrape_basketball_reference_advanced(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page: Status code {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table_id = 'advanced'  
    table = soup.find('table', id=table_id)
    
    if not table:
        print(f"Could not find table with id '{table_id}' on the page")
        return None
    
    data = []
    
    headers = []
    header_row = table.select_one('thead tr')
    if header_row:
        headers = [th.get('data-stat', th.text.strip()) for th in header_row.select('th')]
    
    rows = table.select('tbody tr')
    for row in rows:
        if 'class' in row.attrs and 'thead' in row['class']:
            continue
            
        row_data = {}
        cells = row.select('td, th')
        
        for cell in cells:
            stat_name = cell.get('data-stat')
            if stat_name:
                row_data[stat_name] = cell.text.strip()
        
        if row_data:
            data.append(row_data)
    
    df = pd.DataFrame(data)
    return df

# Doing the scraping for the past seven seasons' worth of data (to get three seasons before each contract in the contracts df)
def main():
    per_game_urls = ["https://www.basketball-reference.com/leagues/NBA_2025_per_game.html",
                     "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html",
                     "https://www.basketball-reference.com/leagues/NBA_2023_per_game.html",
                     "https://www.basketball-reference.com/leagues/NBA_2022_per_game.html",
                     "https://www.basketball-reference.com/leagues/NBA_2021_per_game.html",
                     "https://www.basketball-reference.com/leagues/NBA_2020_per_game.html",
                     "https://www.basketball-reference.com/leagues/NBA_2019_per_game.html"]
    
    advanced_urls = ["https://www.basketball-reference.com/leagues/NBA_2025_advanced.html",
                     "https://www.basketball-reference.com/leagues/NBA_2024_advanced.html",
                     "https://www.basketball-reference.com/leagues/NBA_2023_advanced.html",
                     "https://www.basketball-reference.com/leagues/NBA_2022_advanced.html",
                     "https://www.basketball-reference.com/leagues/NBA_2021_advanced.html",
                     "https://www.basketball-reference.com/leagues/NBA_2020_advanced.html",
                     "https://www.basketball-reference.com/leagues/NBA_2019_advanced.html"]
    
    per_game = pd.DataFrame()
    advanced = pd.DataFrame()

    # Creating two separate CSVs for per-game and advanced statistics
    for url in per_game_urls:
        print("Scraping NBA per-game data from BR...")
        df = scrape_basketball_reference_per_game(url)
        df['Year'] = url.split('_')[1]
        per_game = pd.concat([per_game, df], ignore_index=True)
        
        if df is not None:
            print(f"Successfully scraped {len(df)} per-game stats.")
        else:
            print("Failed to scrape the data.")

    per_game.to_csv('nba_per_game_stats.csv', index=False)


    for url in advanced_urls:
        print("Scraping NBA advanced data from BR...")
        df = scrape_basketball_reference_advanced(url)
        df['Year'] = url.split('_')[1]
        advanced = pd.concat([advanced, df], ignore_index=True)
        
        if df is not None:
            print(f"Successfully scraped {len(df)} per-game stats.")
        else:
            print("Failed to scrape the data.")

    advanced.to_csv('nba_advanced_stats.csv', index=False)

if __name__ == "__main__":
    main()