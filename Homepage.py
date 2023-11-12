import streamlit as st

from pages import Predict_Churn_From_File, Predict_Churn_From_Scratch, Dashboard

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
    
    page = st.sidebar.selectbox("Select Page", ["Predict Churn From File", "Predict Churn From Scratch", "Dashboard"])
    
    if page == "Predict Churn From File":
        Predict_Churn_From_File.show_predict_churn_from_file()
    elif page == "Predict Churn From Scratch":
        Predict_Churn_From_Scratch.show_predict_page_from_scratch()
    elif page == "Dashboard":
        Dashboard.dashboard()

show_homepage()