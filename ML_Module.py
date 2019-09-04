#importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#importing the dataset
dataset = pd.read_csv('training_data_2_csv_UTF.csv')
ds = dataset
for i in range(0,len(ds.screen_name)):
    if 'bot' in ds.screen_name[i].lower():
        ds.screen_name[i] = 1
    else:
        ds.screen_name[i] = 0
    if 'bot' in ds.name[i].lower():
        ds.name[i] = 1
    else:
        ds.name[i] = 0
X = ds.iloc[:,[6,7,8,10,12,15,16,2,18]].values
y = ds.iloc[:, 19].values

#No Missing Data

#Categorical Data
from sklearn.preprocessing import LabelEncoder
labelencoder_X = LabelEncoder()
X[:,5] = labelencoder_X.fit_transform(X[:,5])
X[:,6] = labelencoder_X.fit_transform(X[:,6])

#No NEED for Splitting the dataset
#from sklearn.model_selection import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)

#Fitting the model into Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=10,criterion='entropy',random_state=0)
classifier.fit(X, y)

# Predicting whether the user is a bot or not
def predict(arr):    
    y_pred = classifier.predict_proba(arr)
    return y_pred


