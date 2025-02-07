import streamlit as st
import pandas as pd
from lunch_menu.db import insert_menu, select_table

st.set_page_config(page_title="Input", page_icon="🖤")
st.markdown("# Input 🍜 ")
st.sidebar.markdown("# Input 🍜 ")


members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}


st.subheader("입력")
menu_name = st.text_input("메뉴 이름", placeholder="예: 김치찌개")
# selectbox 사용
# member_name = st.text_input("먹은 사람", value="jiwon")
member_name = st.selectbox("먹은 사람", list(members.keys()), index = list(members.keys()).index('jiwon'))
# member_id = members 의 키
member_id = members[member_name]

dt = st.date_input("먹은 날짜")

isPress = st.button("메뉴 저장")

if isPress:
    if menu_name and member_id and dt:
        if insert_menu(menu_name, member_id, dt):
            st.success(f"입력 성공")
        else:
            st.error(f"입력 실패")
    else:
        st.warning(f"모든 값을 입력해주세요!")


st.subheader("확인")
select_df = select_table(menu_name, member_name, dt)
select_df
