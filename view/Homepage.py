import streamlit as st

def show_homepage():
    st.title("Revelasi Data: Menemukan Pemicu Churn Pelanggan dan Tindakan Efektifnya")
    st.divider()
    st.markdown("<h2>Barudak Bojongsoang Team 😎</h2>", unsafe_allow_html=True)
    st.write("""Dashboard ini digunakan untuk memprediksi apakah seorang pelanggan akan berhenti berlangganan atau tidak
             berdasarkan kriteria tertentu.""")
    
    st.divider()
    
    value = {
        'Anggota 1' : ["Akmal Muzakki Bakir"],
        'Anggota 2' : ["Muhammad Sya'bani Falif"],
        'Anggota 3' : ["Muhammad Zaki Rabbani"],
    }
    st.table(value)
    st.divider()