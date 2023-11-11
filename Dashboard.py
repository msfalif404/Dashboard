import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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
    fig = px.box(df, x='Churn Label', y='Tenure Months')
    fig.update_layout(title='Box Plot Tenure Months untuk Churn Label = Yes dan Churn Label = No')

    st.plotly_chart(fig)

with st.container():
    fig = px.box(df, x='Churn Label', y='Monthly Purchase')
    fig.update_layout(title='Box Plot Monthly Purchase untuk Churn Label = Yes dan Churn Label = No')

    st.plotly_chart(fig)

with st.container():
    fig = px.box(df, x='Churn Label', y='CLTV')
    fig.update_layout(title='Box Plot CLTV untuk Churn Label = Yes dan Churn Label = No')

    st.plotly_chart(fig)

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

with st.container():
    fig = px.histogram(df, x='Payment Method', color='Churn Label', barmode='group', title='Distribusi Metode Pembayaran')
    fig.update_layout(
        xaxis_title='Payment Method',
        yaxis_title='Count'
    )

    st.plotly_chart(fig)

with st.container():
    fig = px.histogram(df, x='Device Class', color='Churn Label', barmode='group', title='Distribusi Device Class')
    fig.update_layout(
        xaxis_title='Device Class',
        yaxis_title='Count',
    )

    st.plotly_chart(fig)

with st.container():
    fig = px.histogram(df, x='Education Product', color='Churn Label', barmode='group', title='Distribusi Education Product')
    fig.update_layout(
        xaxis_title='Education Product',
        yaxis_title='Count'
    )

    st.plotly_chart(fig)

with st.container():
    fig = px.histogram(df, x='Games Product', color='Churn Label', barmode='group', title='Distribusi Games Product')
    fig.update_layout(
        xaxis_title='Games Product',
        yaxis_title='Count'
    )

    st.plotly_chart(fig)

with st.container():
    fig = px.histogram(df, x='Music Product', color='Churn Label', barmode='group', title='Distribusi Music Product')
    fig.update_layout(
        xaxis_title='Music Product',
        yaxis_title='Count'
    )

    st.plotly_chart(fig)

with st.container():
    fig = px.histogram(df, x='Monthly Purchase', color='Device Class', barmode='overlay', title='Histogram Monthly Purchase dengan Device Class')
    fig.update_layout(
        xaxis_title='Monthly Purchase',
        yaxis_title='Count',
    )

    st.plotly_chart(fig)

with st.container():
    fig = px.histogram(df, x='Monthly Purchase', color='Payment Method', barmode='overlay', title='Histogram Monthly Purchase dengan Payment Method')
    fig.update_layout(
        xaxis_title='Monthly Purchase',
        yaxis_title='Count',
    )

    st.plotly_chart(fig)

quantile = df['Monthly Purchase'].quantile([0.25, 0.5, 0.75])
def categorized_purchased(monthly_purchase):
    if monthly_purchase <= quantile[0.25]:
        return 'Pembelian Rendah'
    elif monthly_purchase <= quantile[0.5]:
        return 'Pembelian Menengah'
    else:
        return 'Pembelian Tinggi'

df['Monthly Purchase Category'] = df['Monthly Purchase'].apply(categorized_purchased)

quartiles = df['CLTV'].quantile([0.25, 0.5, 0.75])
def categorized_cltv(cltv):
    if cltv <= quartiles[0.25]:
        return 'CLTV Rendah'
    elif cltv <= quartiles[0.5]:
        return 'CLTV Menengah'
    else:
        return 'CLTV Tinggi'
df['CLTV Category'] = df['CLTV'].apply(categorized_cltv)

def create_segmentation():
    # Buat kolom baru 'Segment' dengan nilai awal 'Other' untuk semua pelanggan
    df['Segment'] = 'Other'

    # Segment Champions
    df.loc[(df['CLTV Category'] == 'CLTV Tinggi') &
        (df['Monthly Purchase Category'] == 'Pembelian Tinggi') &
        (df['Tenure Months'] >= 37), 'Segment'] = 'Champions'

    # Segment High Potential Customer
    df.loc[(df['CLTV Category'] == 'CLTV Menengah') &
        (df['Monthly Purchase Category'] == 'Pembelian Menengah') &
        (df['Tenure Months'] >= 1), 'Segment'] = 'High Potential Customer'

    # Segment Loyal Customer
    df.loc[(df['CLTV Category'] == 'CLTV Tinggi') &
        (df['Tenure Status'] == 'Pelanggan 5 Tahun'), 'Segment'] = 'Loyal Customer'

    # Segment Promising
    df.loc[(df['CLTV Category'] == 'CLTV Menengah') &
        (df['Monthly Purchase Category'] == 'Pembelian Menengah') &
        ((df['Tenure Status'] == 'Pelanggan 3 Tahun') |
            df['Tenure Status'] == 'Pelanggan 4 Tahun'), 'Segment'] = 'Promising'

    # Segment Need Attention Customer
    df.loc[(df['CLTV Category'] == 'CLTV Rendah') &
        (df['Monthly Purchase Category'] == 'Pembelian Rendah') &
        (df['Tenure Status'] != 'Pelanggan lebih dari 5 Tahun'), 'Segment'] = 'Need Attention Customer'

    # Segment Hibernating
    df.loc[(df['CLTV Category'] == 'CLTV Rendah') &
        (df['Monthly Purchase Category'] == 'Pembelian Rendah') &
        (df['Tenure Status'] == 'Pelanggan 5 Tahun'), 'Segment'] = 'Hibernating'

    # Segment New Customer
    df.loc[(df['Tenure Status'] == 'Pelanggan 1 Tahun') &
        (df['CLTV Category'] == 'CLTV Rendah'), 'Segment'] = 'New Customer'

    # Segment New Customer
    df.loc[(df['Tenure Status'] == 'Pelanggan 2 Tahun') &
        ((df['CLTV Category'] == 'CLTV Rendah') |
            (df['CLTV Category'] == 'CLTV Sedang') |
            (df['CLTV Category'] == 'CLTV Tinggi')), 'Segment'] = 'About To Churn'

    # Tampilkan hasil segmentasi
    segment_df = df[['Customer ID', 'CLTV Category', 'Monthly Purchase Category', 'Tenure Status', 'Segment']]

    return segment_df

segment_df = create_segmentation()

with st.container():
    segment = segment_df.groupby('Segment')['Customer ID'].nunique().reset_index()
    fig = px.pie(segment, values='Customer ID', names='Segment', title='Customer Segmentation')

    st.plotly_chart(fig)