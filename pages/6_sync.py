import streamlit as st
import pandas as pd
import datetime
import lunch_menu.constants as const
import requests

st.set_page_config(page_title="SYNC", page_icon="💞")
st.markdown("# SYNC 💞")
st.sidebar.markdown("#모두의 점심 데이터 비교 합치기")


if st.button("데이터 동기화 하기"):
    
    # API 목록 가지고 오기
    # 그 중 내것 빼고 목록을 순회하면서 나의 df랑 비교하며 없는것을 데이터프레임으로 만들기
    # 데이터 프레임을 순회 하면서 insert 하기
    st.success(f"잔업완료 - 새로운 원천 00 곳에서 총 00 건을 새로 추가 하였습니다.")

