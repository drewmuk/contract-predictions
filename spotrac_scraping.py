import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scraping the data for the contracts signed in a given offseason
def scrape_spotrac_nba_contracts(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page: Status code {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the contract table
    table = soup.select_one('table')
    if not table:
        print("Could not find the contract table on the page")
        return None
    
    data = []
    headers = []
    header_row = table.select_one('thead tr')
    if header_row:
        headers = [th.text.strip() for th in header_row.select('th')]
    
    rows = table.select('tbody tr')
    for row in rows:
        row_data = {}
        cells = row.select('td')
        
        if len(cells) < len(headers):
            continue
        
        for i, cell in enumerate(cells):
            if i < len(headers):
                row_data[headers[i]] = cell.text.strip()
        
        # Add each contract to the overall df
        data.append(row_data)
    
    df = pd.DataFrame(data)
    return df

# Doing the scraping for each of the past four offseasons' contract data
def main():
    urls = ["https://www.spotrac.com/nba/contracts/_/year/2024",
            "https://www.spotrac.com/nba/contracts/_/year/2023",
            "https://www.spotrac.com/nba/contracts/_/year/2022",
            "https://www.spotrac.com/nba/contracts/_/year/2021"]
    
    contracts = pd.DataFrame()
    
    for url in urls:
        print("Scraping NBA contract data from Spotrac...")
        df = scrape_spotrac_nba_contracts(url)
        contracts = pd.concat([contracts, df], ignore_index=True)
        
        if df is not None:
            # Save to CSV
            print(f"Successfully scraped {len(df)} contract records.")
            print("Data saved to 'nba_contracts.csv'")
            
            print("\nPreview of the data:")
            print(df.head())
        else:
            print("Failed to scrape the data.")

    contracts.to_csv('nba_contracts.csv', index=False)

    # Adding a section to find the free agents' names for this upcoming offseason
    free_agent_url = "https://www.spotrac.com/nba/free-agents/_/year/2025"
    free_agents = scrape_spotrac_nba_contracts(free_agent_url)

    if free_agents is not None:
        print(f"Successfully scraped {len(free_agents)} free agent records.")
    else:
        print("Failed to scrape the free agent data.")

    free_agents.to_csv('nba_free_agents.csv', index=False)
    
if __name__ == "__main__":
    main()