import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lunch_menu.db import get_connection
from lunch_menu.db import select_table, insert_menu

st.set_page_config(page_title="Main", page_icon="💜")
st.markdown("# Main page 🐽")
st.sidebar.markdown("# Main page 🐽")

st.title("순신 점심 기록장!")
st.write("""
Today's *LUNCH!*

![img](https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMjA0MThfMTcx%2FMDAxNjUwMjg2NTA2OTUz.KAmjW9nEn4DkwLbDXK9K_PQvPhE1ebEYaVIN8xfyF7Qg._lVvsBJN7gsdkm35f1PExK1LdtcoiMC1qpRjHaOUIJIg.JPEG.exo8010%2Fresource%25A3%25A863%25A3%25A9.jpg&type=sc960_832)""")


