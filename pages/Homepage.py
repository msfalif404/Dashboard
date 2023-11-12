import streamlit as st

def show_homepage():
    st.title("Customer Churn Prediction")
    st.write("""Dashboard ini digunakan untuk memprediksi apakah seorang pelanggan akan berhenti berlangganan atau tidak.""")
    
    st.divider()
    
    value = {
        'Nama' : ['Akmal Muzakki Bakir', 'Muhammad Syabani Falif', 'Muhammad Zaki Rabbani']
    }
    st.table(value)
    
    st.divider()
    
    # st.write("""Dataset yang digunakan berasal dari [Kaggle](https://www.kaggle.com/blastchar/telco-customer-churn).""")
    
show_homepage()