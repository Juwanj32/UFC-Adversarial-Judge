# to not overwhelm the reader I have put the code first and after the code there is a box of comments explaining whats going on, as to not clutter the code 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import shap 


# line 2 | start the file by importing pandas and aliasing it so that its less typing | allows us to load the  UFC CSV and treat it like a table (called a DataFrame) so we can filter, sort, and clean it.
# line 3 | its a utility function from scikit-Learn and We need to split our data into 2 defined groups This function shuffles the fights and divides them so the model doesn't just memorize the answers
# line 4 | The type of model im gonna be training which is a collection of decision tree's and its great for tabular data 
# Line 5 | Open-source platform to debug and evaluate NLP (natural language processing), image, and tabular AI models.

# LOAD DATA
df = pd.read_csv('ufc-adversarial-judge/data/ufc_fights.csv')

# line 14 | dataframe assigned to pandas reading a csv of data for the ufc fights | df holds all of UFC history 

# STAT SELECTION 

features = {'R_avg_sig_strk_landed', 'L_avg_sig_strk_landed', 'R_reach_cms', 'L_reach_cms' }
X = df[features].fillna(0)
Y = df['winner']

# line 20 | features are categories in the stats we want the model to focus on to make a guess of the winner 
# line 21 | assign variable to  a single feature in the dataframe | we use fillna(0) to make sure we get all usable numbers if blank cells appear
# line 22 | same thing as 20 man, but no fillna and it represents the winner of the fight

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2,random_state = 42)

# line 29 | train_test_split uses the four variables and uses unpacking to give each variable some training features and labels | random_state = 42 is a random seed generator 

# TRAIN MODEL 
model = RandomForestClassifier(n_estimators = 100)
model.fit = (X_train, y_train)

# line 34 | assiging to a variable called model a 100 differentdecision trees to decide the winner 
# line 35 | .fit looks for patterns betweens the stats and winners 

# SHAP
explain = shap.TreeExplainer(model)
shap_values = explain.shap_values(X_test)

# line 41 | when the random forest classifier makes the decision trees its not able to be read by humans since its tiny math equations | treeExplainer translates this information so we can understand it 
# line 42 | the shap value is where a score is assesed to every stat that explains how one fighter can have an 80% chance to win, while another has 20% chance | X_test is the trained result of the data trained in X_train