import streamlit as st

def show_homepage():
    st.title("Customer Churn Prediction")
    st.write("""Dashboard ini digunakan untuk memprediksi apakah seorang pelanggan akan berhenti berlangganan atau tidak.""")
    
    st.divider()
    
    value = {
        'Anggota 1' : ["Akmal Muzakki Bakir"],
        'Anggota 2' : ["Muhammad Sya'bani Falif"],
        'Anggota 3' : ["Muhammad Zaki Rabbani"],
    }
    st.table(value)
    st.divider()