import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle

# from lightgbm import LGBMClassifier, LGBMRegressor

# from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, KFold, RandomizedSearchCV

import warnings
warnings.filterwarnings("ignore")

with open('model.pkl', 'rb') as file:
    data = pickle.load(file)

tabel = pd.DataFrame({
    'Location': ['Jakarta'],
    'Tenure Months': [1],
    'Device Class': ['High End'],
    'Games Product': ['No'],
    'Music Product': ['No'],
    'Education Product': ['No'],
    'Call Center': ['No'],
    'Payment Method': ['Pulsa'],
    'Video Product': ['No'],
    'Use MyApp': ['No'],
    'Monthly Purchase': [50]
})

tabel['Location'] = data['LocationEncoder'].transform(tabel['Location'])
tabel['Device Class'] = data['DeviceEncoder'].transform(tabel['Device Class'])
tabel['Games Product'] = data['GamesEncoder'].transform(tabel['Games Product'])
tabel['Music Product'] = data['MusicEncoder'].transform(tabel['Music Product'])
tabel['Education Product'] = data['EducationEncoder'].transform(tabel['Education Product'])
tabel['Call Center'] = data['CallCenterEncoder'].transform(tabel['Call Center'])
tabel['Payment Method'] = data['PaymentEncoder'].transform(tabel['Payment Method'])
tabel['Video Product'] = data['VideoEncoder'].transform(tabel['Video Product'])
tabel['Use MyApp'] = data['MyAppEncoder'].transform(tabel['Use MyApp'])

churn_prediction = data['LGBM_Churn'].predict_proba(tabel)
if churn_prediction[0][1] >= 0.5:
    print(f"Churn: Yes, dengan persentase Yes: {round(churn_prediction[0][1], 2)*100}%")
    print(f"Dengan nilai CLTV: {round(data['AdaBoost_CLTV'].predict(tabel)[0], 2)}")
else:
    print(f"Churn: No, dengan persentase No: {round(churn_prediction[0][0], 2)*100}%")
    print(f"Dengan nilai CLTV: {round(data['AdaBoost_CLTV'].predict(tabel)[0], 2)}")