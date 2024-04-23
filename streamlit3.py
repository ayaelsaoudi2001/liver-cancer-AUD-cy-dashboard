import streamlit as st 
from streamlitpage import show_liver_cancer_page
from streamlit2 import show_AUD_page

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Liver Cancer Rates in Cyprus", "Alcohol Use Disorder Rates in Cyprus"])

    if page == "Liver Cancer Rates in Cyprus":
        show_liver_cancer_page()
    elif page == "Alcohol Use Disorder Rates in Cyprus":
        show_AUD_page()

if __name__ == "__main__":
    main()
