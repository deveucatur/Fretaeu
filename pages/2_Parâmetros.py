import streamlit as st
from PIL import Image


icone = Image.open('icone.png')
st.set_page_config(
    page_title="Parâmetros|FretaEU Precificação",
    page_icon=icone,
    layout="wide")

st.image(Image.open("icone.png"), width=180)