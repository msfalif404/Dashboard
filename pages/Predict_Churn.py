import streamlit as st
import pandas as pd
import pickle

st.header('Predicting Customer Churn ✨')


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    dataframe = pd.read_excel(uploaded_file)
    dataframe.rename(columns={'Monthly Purchase (Thou. IDR)' : 'Monthly Purchase', 'CLTV (Predicted Thou. IDR)' : 'CLTV'}, inplace=True)
    columns_tobe_dropped = ['Customer ID', 'Longitude', 'Latitude'  ]
    dataframe = dataframe.drop(columns=columns_tobe_dropped, errors='ignore')

    kolom = ['Games Product', 'Music Product', 'Education Product', 'Video Product', 'Use MyApp']
    for i in kolom:
        dataframe[i] = dataframe[i].replace('No internet service', 'No')

    ### Model
    with open('./model.pkl', 'rb') as file:
        data = pickle.load(file)
        
        dataframe['Location'] = data['LocationEncoder'].transform(dataframe['Location'])
        dataframe['Device Class'] = data['DeviceEncoder'].transform(dataframe['Device Class'])
        dataframe['Games Product'] = data['GamesEncoder'].transform(dataframe['Games Product'])
        dataframe['Music Product'] = data['MusicEncoder'].transform(dataframe['Music Product'])
        dataframe['Education Product'] = data['EducationEncoder'].transform(dataframe['Education Product'])
        dataframe['Call Center'] = data['CallCenterEncoder'].transform(dataframe['Call Center'])
        dataframe['Payment Method'] = data['PaymentEncoder'].transform(dataframe['Payment Method'])
        dataframe['Video Product'] = data['VideoEncoder'].transform(dataframe['Video Product'])
        dataframe['Use MyApp'] = data['MyAppEncoder'].transform(dataframe['Use MyApp'])
        
        churn_prediction = data['LGBM_Churn'].predict_proba(dataframe)
        churn_probabilities = churn_prediction[:, 1]

        dataframe['CLTV Prediction'] = 0

        dataframe['Churn Prediction'] = ['Yes' if prob >= 0.5 else 'No' for prob in churn_probabilities]
        for i in range(1, len(dataframe)):
            dataframe['CLTV Prediction'] = round(data['AdaBoost_CLTV'].predict(dataframe.iloc[(i-1):i, :])[0], 2)

        dataframe.iloc[1]['CLTV Prediction']