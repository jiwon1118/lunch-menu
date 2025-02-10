import streamlit as st
import matplotlib.pyplot as plt
from lunch_menu.db import get_connection
from lunch_menu.db import select_table, insert_menu

st.set_page_config(page_title="Best", page_icon="🧡")
st.markdown("# Best👍")
st.sidebar.markdown("# Best👍")

select_df = select_table()

st.subheader("인기 메뉴 top 10")

not_na_rdf = select_df[~select_df['menu_name'].isin(['-','<결석>','x'])]
gdf = not_na_rdf.groupby('menu_name')['menu_name'].count().reset_index(name='count')
gdf_sorted = gdf.sort_values(by='count', ascending=False)

sdf = gdf_sorted.head(10)
st.write(sdf)

st.subheader("인기 메뉴 top 10 차트")
try:
    fig, ax = plt.subplots(figsize=(10,6))
    sdf.plot(x="menu_name", y="count", kind="bar", ax=ax)
    ax.set_xlabel("Menu Name")
    ax.set_ylabel("Count")
    ax.set_title("Top 10 Popular Menu")
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다.")
    print(f"Exception:{e}")
