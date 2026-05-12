Data Pipeline
1. Scraping & Acquisition
The scraper performs a systematic crawl of UFCStats.com.

Anti-Bot Protection: Implemented randomized delays (1.0s - 2.5s) to mimic human behavior.

Metric Conversion: Automatically converts Imperial measurements (Feet/Inches) to Metric (CM) for better model performance.

2. Cleaning & Engineering
Raw data is processed to remove noise:

Filtering: Removes fighters with 0-0 records to ensure the model learns from active competitors.

Imputation: Replaces 0.0 values in key performance stats with the Median of the dataset.

Win Ratio: Creates a calculated feature: wins / (wins + losses + 0.001).

3. Machine Learning (Random Forest)
The model predicts career success based on physical and technical attributes.

Feature Importance: The project outputs a ranking of features to explain the "AI Judge's" logic (e.g., how much the model weights reach vs. strike accuracy).

How to Run
Scrape Data:

Bash
python scripts/scraper.py
Clean Data:

Bash
python scripts/data_cleaning.py
Train Model:

Bash
python scripts/train_model.py
📈 Roadmap
[x] Build A-Z Fighter Scraper

[x] Implement Automated Data Cleaning

[x] Train Initial Random Forest Model

[ ] Scale Scraper to 4,000+ fighters

[ ] Implement SHAP values for deeper model explainability

[ ] Build a "Fighter Comparison" tool

Developed as part of a Computer Science portfolio focused on Data Engineering and Machine Learning.
