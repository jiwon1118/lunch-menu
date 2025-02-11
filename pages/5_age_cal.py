import streamlit as st
import requests
import lunch_menu.constants as const

st.set_page_config(page_title="API", page_icon="🍽️")

st.markdown("# 나이 계산기🧮")
st.sidebar.header("나이 계산기🧮")


dt = st.date_input("생일 입력") #min_value=None, max_value=None
if st.button("메뉴 저장"):
    headers = {
        'accept': 'application/json'
    }
    r = requests.get(f"{const.API_AGE}/{dt}", headers=headers)
    if r.status_code == 200:
        # TODO age 받아오기
        data = r.json()
        age = data['age']
        st.success(f"{dt}일생의 나이는 {age}살 입니다.")
    else:
        st.error(f"문제가 발생하였습니다. 관리자 문의: {r.status_code}")