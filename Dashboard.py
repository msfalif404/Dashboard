import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from helper.categorize_tenure import categorize_tenure
from sklearn.cluster import KMeans

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

@st.cache_data
def show_tenure_total():
    fig = px.bar(df_churn_all, x='Tenure Status', y='Total Customer', color='Churn Label', barmode='group')
    fig.update_layout(title='Customer Churn Based On Tenure Month')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    show_tenure_total()

@st.cache_data
def show_churn_boxplot():
    fig = px.box(df, x='Churn Label', y='Tenure Months')
    fig.update_layout(title='Box Plot Tenure Months untuk Churn Label = Yes dan Churn Label = No')

    st.plotly_chart(fig)
 
with st.container():
    show_churn_boxplot()

@st.cache_data
def show_monthly_purchase_boxplot():
    fig = px.box(df, x='Churn Label', y='Monthly Purchase')
    fig.update_layout(title='Box Plot Monthly Purchase untuk Churn Label = Yes dan Churn Label = No')

    st.plotly_chart(fig)

with st.container():
    show_monthly_purchase_boxplot()
   
@st.cache_data
def show_cltv_boxplot():
    fig = px.box(df, x='Churn Label', y='CLTV')
    fig.update_layout(title='Box Plot CLTV untuk Churn Label = Yes dan Churn Label = No')

    st.plotly_chart(fig)

with st.container():
    show_cltv_boxplot()

@st.cache_data
def create_correlations():
    corr_df = df.copy()
    corr_df['Churn Label'].replace({'Yes': 1, 'No': 0}, inplace=True)

    dummies = pd.get_dummies(corr_df[['Churn Label', 'Device Class', 'Games Product', 'Music Product',
                                    'Education Product', 'Call Center', 'Video Product', 'Use MyApp',
                                    'Payment Method']])

    df_dummies = pd.DataFrame({'Feature': dummies.columns,
                            'Correlation': dummies.corr()['Churn Label']
                            }).sort_values(by='Correlation', ascending=False)

    bar = go.Bar(x=df_dummies['Feature'][1:], y=df_dummies['Correlation'][1:])

    layout = go.Layout(title='Korelasi Data Kategorikal dengan Customer yang Churn',
                    xaxis=dict(title='Fitur'),
                    yaxis=dict(title='Korelasi'),
                    height=800)

    fig = go.Figure(data=bar, layout=layout)
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')

    return fig
    
with st.container():
    fig = create_correlations()
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def show_payment_method_distribution():
    fig = px.histogram(df, x='Payment Method', color='Churn Label', barmode='group', title='Distribusi Metode Pembayaran')
    fig.update_layout(
        xaxis_title='Payment Method',
        yaxis_title='Count'
    )

    st.plotly_chart(fig)
    
with st.container():
    show_payment_method_distribution()

@st.cache_data
def show_device_class_distribution():
    fig = px.histogram(df, x='Device Class', color='Churn Label', barmode='group', title='Distribusi Device Class')
    fig.update_layout(
        xaxis_title='Device Class',
        yaxis_title='Count',
    )

    st.plotly_chart(fig)

with st.container():
    show_device_class_distribution()
    
@st.cache_data    
def show_education_product_distribution():
    fig = px.histogram(df, x='Education Product', color='Churn Label', barmode='group', title='Distribusi Education Product')
    fig.update_layout(
        xaxis_title='Education Product',
        yaxis_title='Count'
    )

    st.plotly_chart(fig)

with st.container():
    show_education_product_distribution()

@st.cache_data
def show_games_product_distribution():
    fig = px.histogram(df, x='Games Product', color='Churn Label', barmode='group', title='Distribusi Games Product')
    fig.update_layout(
        xaxis_title='Games Product',
        yaxis_title='Count'
    )

    st.plotly_chart(fig)

with st.container():
    show_games_product_distribution()

@st.cache_data
def show_music_product_distribution():
    fig = px.histogram(df, x='Music Product', color='Churn Label', barmode='group', title='Distribusi Music Product')
    fig.update_layout(
        xaxis_title='Music Product',
        yaxis_title='Count'
    )

    st.plotly_chart(fig)

with st.container():
    show_music_product_distribution()

@st.cache_data
def show_histogram_monthly_device_purchase():
    fig = px.histogram(df, x='Monthly Purchase', color='Device Class', barmode='overlay', title='Histogram Monthly Purchase dengan Device Class')
    fig.update_layout(
        xaxis_title='Monthly Purchase',
        yaxis_title='Count',
    )

    st.plotly_chart(fig)

with st.container():
    show_histogram_monthly_device_purchase()

@st.cache_data
def show_histogram_monthly_payment_purchase():
    fig = px.histogram(df, x='Monthly Purchase', color='Payment Method', barmode='overlay', title='Histogram Monthly Purchase dengan Payment Method')
    fig.update_layout(
        xaxis_title='Monthly Purchase',
        yaxis_title='Count',
    )

    st.plotly_chart(fig)

with st.container():
    show_histogram_monthly_payment_purchase()
   
quantile = df['Monthly Purchase'].quantile([0.25, 0.5, 0.75])
@st.cache_data
def categorized_purchased(monthly_purchase):
    if monthly_purchase <= quantile[0.25]:
        return 'Pembelian Rendah'
    elif monthly_purchase <= quantile[0.5]:
        return 'Pembelian Menengah'
    else:
        return 'Pembelian Tinggi'

df['Monthly Purchase Category'] = df['Monthly Purchase'].apply(categorized_purchased)

quartiles = df['CLTV'].quantile([0.25, 0.5, 0.75])
@st.cache_data
def categorized_cltv(cltv):
    if cltv <= quartiles[0.25]:
        return 'CLTV Rendah'
    elif cltv <= quartiles[0.5]:
        return 'CLTV Menengah'
    else:
        return 'CLTV Tinggi'
df['CLTV Category'] = df['CLTV'].apply(categorized_cltv)

@st.cache_resource
def create_clustering_model_cltv():
    X = df.iloc[:, [1, 15]].values
    kmeans = KMeans(n_clusters = 3, init = 'k-means++', random_state = 42)
    y_kmeans = kmeans.fit_predict(X)

    return y_kmeans

df['Cluster'] = create_clustering_model_cltv()

@st.cache_data
def label_cluster(row):
    if row['Cluster'] == 0:
        return 'High-Value Long-Term Customers'
    elif row['Cluster'] == 1:
        return 'Low-Value Short-Term Customers'
    elif row['Cluster'] == 2:
        return 'Mid-Value Mid-Term Customers'
    else:
        return 'Other'

df['CLTV Label'] = df.apply(label_cluster, axis=1)

with st.container():
    data = {
        'Customer Type': df[df['Churn Label'] == 'No']['CLTV Label'].value_counts().index,
        'Count': df[df['Churn Label'] == 'No']['CLTV Label'].value_counts().values
    }
    pie_cltv_label_df = pd.DataFrame(data)
    fig = px.pie(pie_cltv_label_df, names='Customer Type', values='Count', title='Distribusi Retain Customer Segmentation By CLTV')

    st.plotly_chart(fig)

@st.cache_resource
def create_clustering_model_monthly():
    X = df.iloc[:, [1, 11]].values
    kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
    y_kmeans = kmeans.fit_predict(X)

    return y_kmeans

df['Cluster'] = create_clustering_model_monthly()

def label_clusters(row):
    if row['Cluster'] == 0:
        return "Low Purchase Short-Term Customers"
    elif row['Cluster'] == 1:
        return "High Purchase Short-Term Customers"
    elif row['Cluster'] == 2:
        return "Low Purchase Long Term Customers"
    elif row['Cluster'] == 3:
        return "High Purchase Long-Term Customers"
    else:
        return "Other"

df['Monthly Purchase Label'] = df.apply(label_clusters, axis=1)

with st.container():
    data = {
        'Customer Type': df[df['Churn Label'] == 'No']['Monthly Purchase Label'].value_counts().index,
        'Count': df[df['Churn Label'] == 'No']['Monthly Purchase Label'].value_counts().values
    }
    pie_cltv_label_df = pd.DataFrame(data)
    fig = px.pie(pie_cltv_label_df, names='Customer Type', values='Count', title='Distribusi Retain Customer Segmentation By Monthly Purchase')

    st.plotly_chart(fig)
