import streamlit as st
from streamlit_option_menu import option_menu

# --- SIDEBAR MENU ---
menu_items = ["Upload Data", "Data Masker", "Rekomendasi"]
selection = st.sidebar.radio("Menu", menu_items)

# --- PAGE CONFIGURATION ---
page_title = "Rekomendasi Merek Masker"
page_icon = ":money_with_wings:"
layout = "wide"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

# --- PAGE CONTENT ---
st.title(page_title + " " + page_icon)

if selection == "Upload Data":
    st.write("Konten untuk menu 'Upload Data' ditampilkan di sini.")
elif selection == "Data Masker":
    st.write("Konten untuk menu 'Data Masker' ditampilkan di sini.")
elif selection == "Rekomendasi":
    st.write("Konten untuk menu 'Rekomendasi' ditampilkan di sini.")
