import streamlit as st
import pandas as pd
from lunch_menu.db import get_connection, insert_menu, select_table

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


# 오늘  점심 임력 안 한사람을 알 수 있는 버튼 만들기

isPress = st.button("오늘의 점심을 입력 안한 사람")
query = """
SELECT
    m.name,
    count(l.id) as ctid
FROM
    member m
    LEFT JOIN lunch_menu l
    ON l.member_id = m.id
    AND l.dt = CURRENT_DATE
GROUP BY
    m.id,
    m.name
HAVING
    count(l.id) = 0
ORDER BY
    ctid desc
;
"""
if isPress:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            st.write("모두 입력 했습니다")
        else:
            # 이름만 추출하여 리스트로 변환
            names = [row[0] for row in rows]
            # 리스트를 하나의 문자열로 결합
            names_str = ", ".join(names)
            st.success(f"범인은?!:  {names_str} 입니다.")

    except Exception as e:
        st.warning(f"조회 중 오류가 발생했습니다")
        print(f"Exception: {e}")


st.subheader("확인")
select_df = select_table()
select_df
