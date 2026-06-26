# Predicting Football Match Outcomes Using Machine Learning

## Description
This project investigates whether machine learning models can effectively predict English Premier League football match outcomes. It establishes a rigorous, reproducible evaluation framework comparing multiple classification approaches, feature engineering strategies, and class imbalance handling techniques across both **binary** (Home Win / Away Win) and **multiclass** (Home Win / Draw / Away Win) prediction tasks.

The data pipeline utilizes **8 seasons of historical data (2016/17–2024/25)** sourced from *football-data.co.uk* and *elofootball.com*, capturing detailed team statistics, historical match results, and baseline market indicators (Bet365 odds).

### Project Pipeline & Methodology
The experiment is structured into five distinct phases:
1. **Data Collection & Preprocessing:** Compiling multi-season data, handling missing variables, and encoding categorical trends. Data is split into an 80% training and 20% testing framework.
2. **Feature Engineering:** Engineering high-signal domain metrics, including:
   * **Elo Ratings:** Team strengths dynamically scaled after each match based on expected vs. actual outcomes (K-factor scaling).
   * **Attack & Defence Strengths:** Relative performance indices calculated dynamically.
   * **Form & Trend Aggregations:** Generating rolling averages of team metrics to capture momentum.
3. **Dimensionality Reduction & Selection:** Side-by-side comparison of **Boruta feature selection** versus **Principal Component Analysis (PCA)**.
4. **Model Training & Hyperparameter Optimization:** Implementing Grid Search and Random Search across six distinct classification architectures, incorporating manual class weighting and sample weight computations to address class imbalances.
5. **Evaluation:** Diagnostic profiling using Multiclass/Binary Accuracy, Precision, Recall, $F_1$-Score, and learning curve stability.

### Key Analytical Findings
* **The Elo Signal:** Feature importance analysis consistently identified `Diff_HomeEloBefore` (the pre-match Elo rating differential) as the single most predictive variable across all models.
* **Home Advantage Quantified:** Home-based performance metrics ranked significantly higher than away equivalents across all models, providing quantitative validation of the home-ground advantage.
* **Feature Strategy Performance:** PCA systematically outperformed Boruta when paired with linear models by successfully resolving severe feature multicollinearity. Conversely, non-linear tree-based models exhibited a marginal performance preference for the original Boruta-selected feature sets.
* **The Draw Bottleneck:** Class balancing proved vital for multiclass stabilization but unnecessary for binary tasks. However, predicting draws remains an unresolved challenge—several models yielded near-zero recall for draws even after balancing, indicating that draw outcomes lack distinct feature-space separability within historical aggregations.

---

## Predictive Modeling Performance

### 1. Boruta Feature Set Evaluation
| Model Configuration | Multiclass Accuracy | Binary Accuracy |
| :--- | :---: | :---: |
| **Logistic Regression** | **0.5595** *(Best)* | 0.7126 |
| **Linear SVC (Stratified)** | 0.5560 | 0.7425 |
| **Linear SVC (Balanced)** | 0.4956 | **0.7471** *(Best)* |
| **ELM Neural Network** | 0.5560 | 0.7333 |
| **RBF SVM** | 0.5506 | 0.7379 |
| **XGBoost** | 0.5435 | 0.7379 |
| **Random Forest** | 0.5435 | 0.7379 |

### 2. PCA Feature Set Evaluation
| Model Configuration | Multiclass Accuracy | Binary Accuracy |
| :--- | :---: | :---: |
| **Linear SVC (Stratified)** | **0.5684** *(Best)* | 0.7425 |
| **Linear SVC (Balanced)** | 0.5151 | **0.7471** *(Best)* |
| **ELM Neural Network** | 0.5613 | 0.7103 |
| **Logistic Regression** | 0.5560 | 0.7471 |
| **RBF SVM** | 0.5524 | 0.7218 |
| **Random Forest** | 0.5435 | 0.7379 |
| **XGBoost** | 0.5204 | 0.7310 |

---

## Usage

### Prerequisites
The experimental notebooks run inside a standard Python data science environment. The core dependencies include:
* **Python 3.x**
* **Jupyter Notebook / Google Colab**
* **NumPy & Pandas** (Data manipulation)
* **Scikit-learn** (Linear models, SVM, KNN, PCA, Evaluation)
* **XGBoost** (Gradient boosting)
* **Boruta** (Feature selection wrapper)

### Running the Project
1. Download the Mainfile to view results and see code.
