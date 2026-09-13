import streamlit as st

st.title("Hoşgeldin!")
st.markdown(
    """ 
    Başvurduğun ilan için ne kadar uyumlu olduğunu görmek \n
    Eksik yönlerini iyileştirmek,\n
    Artı yönlerini öğrenmek,\n
    Ve hangi ilanların zaman kaybı olduğunu görmek mi istiyorsun?\n
    Job Analyze AI bunun için var. 
    """
)

if st.button("Analiz Et"):
    st.balloons()