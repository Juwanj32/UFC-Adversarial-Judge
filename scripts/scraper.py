#inspired by asaniczka
# ==========================================
# 1. SETUP AND DEPENDENCIES
# ==========================================
import string
import time 
import random
import datetime
import re
import os
import logging
import requests
from bs4 import BeautifulSoup
from icecream import ic

# --- DECISION: PROJECT STRUCTURE ---
# Creating a dedicated folder structure ensures that raw data doesn't 
# clutter your script directory and keeps logs separate for debugging.
PROJECT_NAME = 'ufc_ai_judge_dataset'
os.makedirs(f"{PROJECT_NAME}/data", exist_ok=True)
os.makedirs(f"{PROJECT_NAME}/logs", exist_ok=True)

# ==========================================
# 2. FEATURE ENGINEERING HELPERS
# ==========================================

def convert_height_to_cm(height_str):
    """
    DECISION: Convert Imperial to Metric (cm).
    Why: For your 'Concussion Vision Safety System', skeletal landmark 
    calculations are significantly easier in metric units than feet/inches.
    """
    if not height_str or "--" in height_str:
        return None # DECISION: Use None for missing data to allow scikit-learn Imputers to handle it.
    try:
        # Regex extracts all numbers. e.g., "5' 11\"" -> [5, 11]
        feet, inches = map(int, re.findall(r'\d+', height_str))
        total_inches = (feet * 12) + inches
        return round(total_inches * 2.54, 2)
    except Exception:
        return None

def convert_reach_to_cm(reach_str):
    """
    DECISION: Metric reach.
    Why: Reach is a high-correlation feature for AI judges. Converting to CM 
    standardizes it with height for ratio based feature engineering.
    """
    if not reach_str or "--" in reach_str:
        return None
    try:
        inches = float(re.search(r'\d+', reach_str).group())
        return round(inches * 2.54, 2)
    except Exception:
        return None

# ==========================================
# 3. CORE SCRAPER LOGIC
# ==========================================

def scrape_fighter_details(url):
    """
    DECISION: Request-based scraping with BeautifulSoup.
    Why: UFCStats.com is server-side rendered, so we don't need a heavy 
    tool like Selenium. Requests + BS4 is faster and lighter for large datasets.
    """
    try:
        # DECISION: Set a timeout. Scrapers often hang on dead links; 10s is safe.
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # --- EXTRACT NAME & RECORD ---
        name = soup.select_one('.b-content__title-highlight').get_text(strip=True)
        record_text = soup.select_one('.b-content__title-record').get_text(strip=True)
        # DECISION: Parse record (W-L-D) into separate integers.
        # This allows the AI to calculate 'Win Percentage' or 'Experience Level'.
        record_nums = re.findall(r'\d+', record_text)
        wins, losses, draws = map(int, record_nums[:3])

        # --- EXTRACT PHYSICAL STATS (BIO) ---
        # DECISION: Select the 'small-width' box specifically.
        # This box contains Height, Weight, Reach, Stance, and DOB.
        bio_items = soup.select('.b-list__info-box_style_small-width .b-list__box-list-item')
        bio_clean = [item.get_text(strip=True) for item in bio_items]
        
        # --- EXTRACT CAREER STATS (PERFORMANCE) ---
        # DECISION: Convert percentages (e.g. 45%) to floats (0.45).
        # Machine learning models (like scikit-learn) perform better with 
        # normalized floats than with strings or large integers.
        career_items = soup.select('.b-list__info-box_style_middle-width .b-list__box-list-item')
        stats = {}
        for item in career_items:
            t = item.get_text(strip=True)
            if 'SLpM:' in t: stats['strikes_landed_min'] = float(t.split(':')[-1])
            if 'Str. Acc.:' in t: stats['strike_accuracy'] = float(t.split(':')[-1].replace('%','')) / 100
            if 'SApM:' in t: stats['strikes_absorbed_min'] = float(t.split(':')[-1])
            if 'Str. Def:' in t: stats['strike_defense'] = float(t.split(':')[-1].replace('%','')) / 100
            if 'TD Avg.:' in t: stats['takedown_avg'] = float(t.split(':')[-1])
            if 'TD Acc.:' in t: stats['takedown_accuracy'] = float(t.split(':')[-1].replace('%','')) / 100

        # DECISION: Return a Flat Dictionary.
        # This makes it trivial to convert the final list into a Pandas DataFrame.
        return {
            "name": name,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "height_cm": convert_height_to_cm(bio_clean[0]),
            "reach_cm": convert_reach_to_cm(bio_clean[2]),
            "stance": bio_clean[3].replace('Stance:', '').strip() or "Orthodox",
            **stats
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# ==========================================
# 4. EXECUTION FLOW
# ==========================================

def main():
    # DECISION: Systematic Alphabetical Crawl.
    # The site organizes fighters by the first letter of their last name.
    # We iterate through A-Z to ensure we don't miss any fighters.
    all_fighter_urls = []
    print("Fetching fighter links...")
    
    for char in string.ascii_lowercase:
        url = f"http://ufcstats.com/statistics/fighters?char={char}&page=all"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # DECISION: Targeted CSS Selectors.
        # We only want links that lead to 'fighter-details' to avoid ads/nav links.
        links = [a['href'] for a in soup.select('tr.b-statistics__table-row a') if 'fighter-details' in a['href']]
        all_fighter_urls.extend(list(set(links))) # Use set() to remove duplicates
        
    # DECISION: Limit scraping for testing.
    # Set this to len(all_fighter_urls) when you are ready to build the full AI dataset.
    LIMIT = 20 
    final_dataset = []

# ... inside your main scraping loop ...
for i, link in enumerate(fighter_links):
    # Your existing scraping logic here
    # ic(f"Scraping {i+1}/{len(fighter_links)}")
    
    # ADD THIS: The "Human" Delay
    # Scraping 4,000+ fighters is a lot. 
    # Let's wait between 1 and 2.5 seconds between every fighter.
    time.sleep(random.uniform(1.0, 2.5))
    
    # PRO TIP: Save progress every 50 fighters in case your internet drops
    if (i + 1) % 50 == 0:
        ic(f"Checkpoint: {i+1} fighters scraped. Saving progress...")
        
#turns information from scraper into csv for AI to read 

# After your scraper finishes gathering 'final_dataset'
df = pd.DataFrame(final_dataset)

# Clean the stance column as we discussed
df['stance'] = df['stance'].str.replace('STANCE:', '')

# Save it to your data folder
df.to_csv('data/raw/fighter_stats.csv', index=False)
ic("File saved to data/raw/fighter_stats.csv")


        
    # DECISION: Print first entry to verify structure.
    if final_dataset:
        ic(final_dataset[0])

if __name__ == "__main__":
    main()
    
#turns information from scraper into csv for AI to read 

# After your scraper finishes gathering 'final_dataset'
df = pd.DataFrame(final_dataset)

# Clean the stance column as we discussed
df['stance'] = df['stance'].str.replace('STANCE:', '')

# Save it to your data folder
df.to_csv('data/raw/fighter_stats.csv', index=False)
ic("File saved to data/raw/fighter_stats.csv")

