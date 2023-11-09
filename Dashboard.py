import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from helper.categorize_tenure import categorize_tenure

# Reading The Dataset
df = pd.read_excel('telco_dataset.xlsx')
df.rename(columns={'Monthly Purchase (Thou. IDR)' : 'Monthly Purchase', 'CLTV (Predicted Thou. IDR)' : 'CLTV'}, inplace=True)

# Categorizing Customer By Tenure Months
df['Tenure Status'] = df['Tenure Months'].apply(categorize_tenure)

# Creating Dataframe Contains All Churned Customer
tenure_class = df['Tenure Status'].unique()
for i in tenure_class:
    df_churn = df[df['Tenure Status'] == i]['Churn Label'].value_counts().reset_index()

    if df_churn.shape[0] == 0:
        df_churn.loc[1] = ['No', 0]
        df_churn.columns = ['Churn Label', 'Total Customer']
    else:
        df_churn.columns = ['Churn Label', 'Total Customer']

    df_churn['Tenure Status'] = i
    df_churn = df_churn[['Tenure Status', 'Churn Label', 'Total Customer']]

    if i == df['Tenure Status'].unique()[0]:
        df_churn_all = df_churn
    else:
        df_churn_all = pd.concat([df_churn_all, df_churn])

st.header('Explanatory Data Analysis ✨')

col1, col2 = st.columns(2)

# Calculating Churn and Retain Percentage
total_customers = df['Customer ID'].nunique()
churn_customers = df[df['Churn Label'] == 'Yes']['Customer ID'].nunique()
retain_customers = df[df['Churn Label'] == 'No']['Customer ID'].nunique()
churn_percentage = (churn_customers / total_customers) * 100
retain_percentage = (retain_customers / total_customers) * 100

with col1:
    st.metric("Customer Retain ✅", value=f"{round(retain_percentage,2)}%")

with col2:
    st.metric("Customer Churn ❌", value=f"{round(churn_percentage,2)}%")

with st.container():
    fig = px.bar(df_churn_all, x='Tenure Status', y='Total Customer', color='Churn Label', barmode='group')
    fig.update_layout(title='Customer Churn Based On Tenure Month')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    corr_df = df.copy()
    corr_df['Churn Label'].replace({'Yes' : 1, 'No' : 0}, inplace=True)

    dummies = pd.get_dummies(corr_df[['Churn Label', 'Device Class', 'Games Product', 'Music Product',
                                    'Education Product', 'Call Center', 'Video Product', 'Use MyApp',
                                    'Payment Method']])

    df_dummies = pd.DataFrame({'Feature': dummies.columns,
                            'Correlation': dummies.corr()['Churn Label']
                            })

    bar = go.Bar(x=df_dummies['Feature'][1:], y=df_dummies['Correlation'][1:])

    layout = go.Layout(title='Korelasi Data Kategorikal dengan Customer yang Churn',
                            xaxis=dict(title='Produk'),
                            yaxis=dict(title='Korelasi'),
                            height=800)

    fig = go.Figure(data=bar, layout=layout)
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)