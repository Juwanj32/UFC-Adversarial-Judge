import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from icecream import ic

# line 1 | Standard data science toolkit to load our cleaned CSV into a structured table (DataFrame).
# line 2 | Shuffles and splits our data so the model can learn on one set and be tested on another.
# line 3 | Instead of a Classifier (Win/Loss), we use a Regressor to predict the numerical quantity of wins.
# line 4 | Math utilities to check how far off the AI's guesses are from the actual fighter records.
# line 5 | A debugging tool that prints variables in a more readable way than standard print().

def train_fighter_model():


    # df.shape returns (rows, columns) — confirms how many fighters actually loaded
    # Catches silent issues like the file being empty or only having 10 rows


    # line 13 | Points the script to the 'processed' folder where our data_cleaning.py saved the polished stats.
    # line 15 | Reads the file; the 'try/except' block prevents a crash if the file is missing.

    data_path = 'data/processed/matchups.csv'
    df = pd.read_csv(data_path)

    X = df.drop(columns=['winner'])   # all 8 difference columns
    y = df['winner']                  # 1 = fighter A wins, 0 = fighter B wins
        
    X = X.dropna()
    y = y[X.index]

    # If any fighter is missing reach_cm or height_cm, the model crashes silently
    # .dropna() removes those rows from X, then we realign y to match the same rows

    # line 23 | features are the specific metrics (the 'DNA') we want the AI Judge to look at.
    # line 24 | X represents the input data; we feed these stats into the model to find patterns.
    # line 25 | y is the answer key; it's the actual number of wins we want the model to learn to predict.

    # 3. THE SPLIT
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # line 31 | Unpacks the data into four variables: 80% for training the brain, 20% for the final exam (testing).
    # line 31 | random_state=42 ensures the "random" shuffle is the same every time we run it for consistency.

    # 4. INITIALIZE AND TRAIN MODEL 
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    ic("Training the Random Forest model...")
    model.fit(X_train, y_train)

    # line 37 | Builds a forest of 100 decision trees that work together to vote on the best prediction.
    # line 39 | .fit is the actual "learning" phase where the trees find the links between stats and wins.

    # 5. EVALUATE (THE TEST)
    predictions = model.predict(X_test)         # ADD THIS LINE FIRST
    acc = accuracy_score(y_test, predictions)
    cm = confusion_matrix(y_test, predictions)
    ic(f"Accuracy: {acc:.4f}")
    ic(f"Confusion matrix:\n{cm}")
    
    # .4f gives R2 four decimal places since it's a small number between 0 and 1

    # line 43 | The model looks at the 20% test stats it has NEVER seen before and makes a guess.
    # line 44 | MAE calculates the average "miss"—e.g., if it says 10 wins and the fighter has 8, the error is 2.
    # line 45 | R2 Score measures how much of the "win" logic the model actually understands (0 to 1 scale).

    # 6. FEATURE IMPORTANCE (THE 'JUDGE' LOGIC)
    importances = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values(by='importance', ascending=False)
    
    ic("Feature Importances (What the AI Judge values most):")
    ic(importances)

    # line 50 | Just like SHAP, this extracts which stat (reach, accuracy, etc.) influenced the trees the most.
    # line 54 | Sorts the results so the most influential "Judicial" factor is at the very top.

if __name__ == "__main__":
    train_fighter_model()