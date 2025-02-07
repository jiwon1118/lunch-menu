import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from lunch_menu.db import get_connection
from lunch_menu.db import select_table, insert_menu

st.set_page_config(page_title="Insert", page_icon="💛")
st.markdown("# Insert 🗄️")
st.sidebar.markdown("# Insert 🗄️")


members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

# CSV로 로드해서 한번에 다 DB에 INSERT 하는거
st.subheader("벌크 인서트")
isPress = st.button("한방에 인서트")


if isPress:
    try:
        df = pd.read_csv('note/menu.csv')
        start_idx = df.columns.get_loc('2025-01-07')
        rdf= df.melt(id_vars=['ename'], value_vars=(df.columns[start_idx:-2]),var_name='dt', value_name='menu')
        not_na_rdf = rdf[~rdf['menu'].isin(['-','<결석>','x'])]

# TODO
# 벌크인서트 버튼이 눌리면  성공/실패 구분해서 완료 메시지 출력하기
        # 총 건수
        total_count = len(not_na_rdf)
        # 성공 건수 + 성공은 insert 하기
        success_count = 0
        for _, row in not_na_rdf.iterrows():
            m_id = members[row['ename']]
            if insert_menu(row['menu'], m_id, row['dt']):
                success_count += 1
        # 실패 건수
        fail_count = total_count - success_count

        if total_count == success_count:
            st.success(f"벌크인서트 성공: 총{total_count}건")
        else:
            st.error(f"총건 {total_count}건중 {fail_count}건 실패")

    except Exception as e:
        st.warning(f"조회 중 오류가 발생했습니다")
        print(f"Exception: {e}")

