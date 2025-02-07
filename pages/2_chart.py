import streamlit as st
import matplotlib.pyplot as plt
from lunch_menu.db import get_connection
from lunch_menu.db import select_table, insert_menu

st.set_page_config(page_title="Chart", page_icon="💛")
st.markdown("# Chart📊")
st.sidebar.markdown("# Chart📊")

select_df = select_table()

st.subheader("통계")

not_na_rdf = select_df[~select_df['menu_name'].isin(['-','<결석>','x'])]
gdf = not_na_rdf.groupby('member_name')['menu_name'].count().reset_index()
gdf

st.subheader("차트")
try:
    fig, ax = plt.subplots()
    gdf.plot(x="member_name", y="menu_name", kind="bar", ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다.")
    print(f"Exception:{e}")
