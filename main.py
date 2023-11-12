import streamlit as st

from view.Predict_Churn_From_File import show_predict_churn_from_file
from view.Predict_Churn_From_Scratch import show_predict_page_from_scratch
from view.Dashboard import show_dashboard
from view.Homepage import show_homepage

page = st.sidebar.selectbox("Select Page", ["Homepage", "Predict Churn From File", "Predict Churn From Scratch", "Dashboard"])

if page == "Homepage":
    show_homepage()
elif page == "Predict Churn From Scratch":
    show_predict_page_from_scratch()
elif page == "Dashboard":
    show_dashboard()
elif page == "Predict Churn From File":
    show_predict_churn_from_file()