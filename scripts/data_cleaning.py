import pandas as pd
import numpy as np

def clean_fighter_data(input_path, output_path):
    # Load the data
    df = pd.read_csv(input_path)
    
    # 1. Drop non-competitors (Remove if they have 0 wins AND 0 losses)
    # This removes "Ghost" profiles that haven't actually fought.
    df = df[~((df['wins'] == 0) & (df['losses'] == 0))]

    # 2. Imputation (Replace 0.0 with the Median)
    # We use median because UFC stats often have outliers that skew the mean.
    cols_to_fix = ['strike_accuracy', 'strike_defense', 'takedown_accuracy', 'takedown_avg']
    
    for col in cols_to_fix:
        # Replace 0.0 with NaN so we can calculate the median properly
        df[col] = df[col].replace(0.0, np.nan)
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)

    # 3. Feature Engineering: Win Ratio
    # We add 1 to the denominator to avoid "Division by Zero" errors (Laplace Smoothing)
    df['win_ratio'] = df['wins'] / (df['wins'] + df['losses'] + 0.001)

    # Save the cleaned data
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    clean_fighter_data('data/raw/fighter_stats.csv', 'data/processed/cleaned_fighters.csv')