import streamlit as st
import pandas as pd
from main import analiz_et

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

ilan_metni = st.text_area("İlan Metnini Buraya Yapıştır")

if st.button("Analiz Et"):
    sonuc = analiz_et(ilan_metni)
    st.write(f"Puan = {sonuc}")