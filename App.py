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


st.subheader("확인")

select_df = select_table()
select_df



st.subheader("통계")

not_na_rdf = select_df[~select_df['menu_name'].isin(['-','<결석>','x'])]
gdf = not_na_rdf.groupby('member_name')['menu_name'].count().reset_index()
gdf

st.subheader("차트")
# matplotlib로 바 차트 그리기
#오류 안 뜨게 하기
try:
    fig, ax = plt.subplots()
    gdf.plot(x="member_name", y="menu_name", kind="bar", ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다.")
    print(f"Exception:{e}") 


# TODO
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
