import pandas as pd
import streamlit as st
import pickle
import numpy as np

def show_predict_page_from_scratch():
    st.header('Predicting Customer Churn ✨')

    LOCATION = [
        'Jakarta',
        'Bandung'
    ]

    DEVICE_CLASS = [
        'High End',
        'Mid End',
        'Low End'
    ]

    GAMES_PRODUCT = [
        'Yes',
        'No'
    ]

    MUSIC_PRODUCT = [
        'Yes',
        'No'   
    ]

    EDUCATION_PRODUCT = [
        'Yes',
        'No'
    ]

    CALL_CENTER = [
        'Yes',
        'No'
    ]

    VIDEO_PRODUCT = [
        'Yes',
        'No'
    ]

    USE_MY_APP = [
        'Yes',
        'No'
    ]

    PAYMENT_METHOD = [
        'Pulsa',
        'Credit',
        'Debit',
        'Digital Wallet'
    ]
    
    tenure = st.slider('Tenure Months', 0, 72)
    location = st.selectbox('Location', LOCATION)
    device_class = st.selectbox('Device Class', DEVICE_CLASS)
    games_product = st.selectbox('Games Product', GAMES_PRODUCT)
    music_product = st.selectbox('Music Product', MUSIC_PRODUCT)
    education_product = st.selectbox('Education Product', EDUCATION_PRODUCT)
    call_center = st.selectbox('Call Center', CALL_CENTER)
    video_product = st.selectbox('Video Product', VIDEO_PRODUCT)
    use_my_app = st.selectbox('Use My App', USE_MY_APP)
    payment_method = st.selectbox('Payment Method', PAYMENT_METHOD)
    monthly_purchase = st.slider('Monthly Purchase', 20, 155)

    with open('model.pkl', 'rb') as file:
        data = pickle.load(file)

    ok = st.button('Prediksi Churn')
    if ok:
        dataframe = pd.DataFrame({
            'Location': [location],
            'Tenure Months': [tenure],
            'Device Class': [device_class],
            'Games Product': [games_product],
            'Music Product': [music_product],
            'Education Product': [education_product],
            'Call Center': [call_center],
            'Payment Method': [payment_method],
            'Video Product': [video_product],
            'Use MyApp': [use_my_app],
            'Monthly Purchase': [monthly_purchase]
        })
        st.write(dataframe)

        # data['LocationEncoder']
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
        if churn_prediction[0][1] >= 0.5:
            st.write(f"Churn: Yes, dengan persentase Yes: {round(churn_prediction[0][1], 2)*100}%")
            st.write(f"Dengan nilai CLTV: {round(data['AdaBoost_CLTV'].predict(dataframe)[0], 2)}")
        else:
            st.write(f"Churn: No, dengan persentase No: {round(churn_prediction[0][0], 2)*100}%")
            st.write(f"Dengan nilai CLTV: {round(data['AdaBoost_CLTV'].predict(dataframe)[0], 2)}")