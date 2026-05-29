# 🤝 Handoff: UFC Adversarial Judge Session

**Date:** May 11, 2026
**Current Branch:** `model-training-logic`

---

## 🎯 The Ultimate Goal
Building an **AI Adversarial Judge** that doesn't just predict fight winners, but "explains" its logic. We are moving from raw data scraping to a sophisticated Random Forest model that identifies which fighter attributes (reach, height, strike volume) have the highest correlation with victory.

## 📊 Current Progress: 65%
- [x] **A-Z Crawler:** Functional (100%)
- [x] **Data Pipeline:** Automated cleaning & Metric conversion (100%)
- [x] **Model Architecture:** Random Forest Regressor implemented (90%)
- [ ] **Data Scaling:** Only 20/4000 fighters scraped (5%)
- [ ] **Explainability:** Feature importance active, SHAP values pending (0%)

## 🛠️ Active Files
- `scripts/train_model.py`: Implementing Random Forest Regressor and evaluation metrics.
- `scripts/data_cleaning.py`: Refining the median imputation and win-ratio logic.
- `data/processed/cleaned_fighters.csv`: The current "Brain" of the project.

## ⚠️ The "Graveyard" (What Failed/Lessons Learned)
* **Failed:** Running `data_cleaning.py` without manually creating the `/processed` directory (Caused `OSError`).
    * *Fix:* Added `mkdir -p` command to the workflow and `os.makedirs` to the script.
* **Failed:** Copy-pasting code blocks from different logic versions (Caused "Undefined Variable" errors for `pd`, `y`, and `final_dataset`).
    * *Fix:* Reorganized code into a structured `main()` function with clear variable scopes.
* **Failed:** Using `RandomForestClassifier` for career win totals.
    * *Fix:* Switched to `RandomForestRegressor` because win totals are continuous numbers, not categories.

## ⏭️ Next Steps
1.  **Massive Scrape:** In the next session, update `LIMIT` in `scraper.py` from 20 to 200+ fighters. This will give the Random Forest enough "experience" to improve the $R^2$ accuracy score.
2.  **Accuracy Audit:** Run `train_model.py` on the larger dataset and check the **Mean Absolute Error (MAE)**. If the error is > 2 wins, we need to add more features.
3.  **SHAP Integration:** Start the next session by importing `shap` to create visual "Force Plots" that show exactly why a specific fighter was predicted to win.
4.  **README Polish:** Update the "Roadmap" section as we complete the scaling phase.

---
**Current Status:** Environment is stable, code is fully documented, and a fresh branch is ready for AI experimentation.
