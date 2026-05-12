import string
import time 
import random
import datetime
import re
import os
import pandas as pd
import logging
import requests
from bs4 import BeautifulSoup
from icecream import ic

# line 1 | Standard library for A-Z characters to crawl the website alphabetically.
# line 2-3 | Time and Random allow us to pause between requests so the UFC site doesn't block our IP.
# line 6 | re (Regular Expressions) is used to extract numbers out of messy strings like "5' 11\"".
# line 8 | Pandas allows us to take the list of fighter dictionaries and turn them into a CSV table.
# line 11 | BeautifulSoup is the "parser" that lets us search through HTML tags to find specific stats.

# --- SETUP ---
PROJECT_NAME = 'ufc_ai_judge_dataset'
os.makedirs(f"data/raw", exist_ok=True) 
os.makedirs(f"{PROJECT_NAME}/logs", exist_ok=True)

# line 16 | Ensures the 'raw' data folder exists so the script doesn't crash when it tries to save the file.

# --- HELPERS ---
def convert_height_to_cm(height_str):
    if not height_str or "--" in height_str:
        return None
    try:
        feet, inches = map(int, re.findall(r'\d+', height_str))
        total_inches = (feet * 12) + inches
        return round(total_inches * 2.54, 2)
    except Exception:
        return None

# line 25 | Converts Imperial to Metric. ML models handle floats (175.26) better than strings (5' 9").

def scrape_fighter_details(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        name = soup.select_one('.b-content__title-highlight').get_text(strip=True)
        record_text = soup.select_one('.b-content__title-record').get_text(strip=True)
        record_nums = re.findall(r'\d+', record_text)
        wins, losses, draws = map(int, record_nums[:3])

        # line 43 | Targets the fighter's name and record (W-L-D) using CSS classes from the UFC site.

        bio_items = soup.select('.b-list__info-box_style_small-width .b-list__box-list-item')
        bio_clean = [item.get_text(strip=True) for item in bio_items]
        
        career_items = soup.select('.b-list__info-box_style_middle-width .b-list__box-list-item')
        stats = {'strikes_landed_min': 0.0, 'strike_accuracy': 0.0, 'strikes_absorbed_min': 0.0, 
                 'strike_defense': 0.0, 'takedown_avg': 0.0, 'takedown_accuracy': 0.0}
        
        # line 53 | Initializes a dictionary with 0.0 to prevent errors if a fighter has no recorded stats.

        for item in career_items:
            t = item.get_text(strip=True)
            if 'SLpM:' in t: stats['strikes_landed_min'] = float(t.split(':')[-1])
            if 'Str. Acc.:' in t: stats['strike_accuracy'] = float(t.split(':')[-1].replace('%','')) / 100
            # ... additional logic for defense and takedowns ...

        # line 57-60 | Loops through the performance table, strips '%' signs, and converts stats to decimals (0.45).

        return {
            "name": name, "wins": wins, "losses": losses, "draws": draws,
            "height_cm": convert_height_to_cm(bio_clean[0]),
            "reach_cm": convert_reach_to_cm(bio_clean[2]),
            "stance": bio_clean[3].replace('Stance:', '').strip() or "Orthodox",
            **stats
        }
    except Exception as e:
        ic(f"Error scraping {url}: {e}")
        return None

# --- MAIN EXECUTION ---
def main():
    all_fighter_urls = []
    print("Fetching fighter links...")
    
    for char in string.ascii_lowercase:
        url = f"http://ufcstats.com/statistics/fighters?char={char}&page=all"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = [a['href'] for a in soup.select('tr.b-statistics__table-row a') if 'fighter-details' in a['href']]
        all_fighter_urls.extend(list(set(links)))

    # line 87-91 | Iterates through pages A to Z to gather every fighter's personal URL.

    all_fighter_urls = list(set(all_fighter_urls))
    LIMIT = 20 
    final_dataset = []
    
    for i, link in enumerate(all_fighter_urls[:LIMIT]):
        data = scrape_fighter_details(link)
        if data:
            final_dataset.append(data)
            ic(f"Scraped {i+1}/{LIMIT}: {data['name']}")
        
        time.sleep(random.uniform(1.0, 2.0))

    # line 102 | Adds a random sleep timer to mimic human browsing and avoid being blacklisted.

    if final_dataset:
        df = pd.DataFrame(final_dataset)
        df['stance'] = df['stance'].str.replace('STANCE:', '')
        output_path = 'data/raw/fighter_stats.csv'
        df.to_csv(output_path, index=False)
        ic(f"Success! File saved to {output_path}")

    # line 106-110 | Final conversion: Turns the list of dictionaries into a CSV file for the AI to use.

if __name__ == "__main__":
    main()