import streamlit as st
import pandas as pd

st.title("Hoşgeldin!")
st.markdown(
    """ 
    Başvurduğun ilan için ne kadar uyumlu olduğunu görmek,
    Eksik yönlerini iyileştirmek,
    Artı yönlerini öğrenmek,
    Ve hangi ilanların zaman kaybı olduğunu görmek mi istiyorsun?
    Job Analyze AI bunun için var. 
    """
)

uploaded_files = st.file_uploader(
    "CV'ni Yükle (PDF)", accept_multiple_files=True, type="pdf"
)
for uploaded_file in uploaded_files:
    cv = pd.read_pdf(uploaded_file)
    st.write(cv)