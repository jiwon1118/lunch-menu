import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg
import os
from dotenv import load_dotenv

st.markdown("# Main page 🐽")
st.sidebar.markdown("# Main page 🐽")

st.title("순신 점심 기록장!")
st.write("""
Today's *LUNCH!*

![img](https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMjA0MThfMTcx%2FMDAxNjUwMjg2NTA2OTUz.KAmjW9nEn4DkwLbDXK9K_PQvPhE1ebEYaVIN8xfyF7Qg._lVvsBJN7gsdkm35f1PExK1LdtcoiMC1qpRjHaOUIJIg.JPEG.exo8010%2Fresource%25A3%25A863%25A3%25A9.jpg&type=sc960_832)""")

load_dotenv()
db_name = os.getenv("DB_NAME")
DB_CONFIG = {
    "user": os.getenv("DB_USERNAME"),
    "dbname": db_name,
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)

def insert_menu(menu_name, member_name, dt):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lunch_menu (menu_name, member_name, dt) VALUES (%s, %s, %s);",
            (menu_name, member_name, dt)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Exception:{e}")
        return False


df = pd.read_csv('note/menu.csv')

st.subheader("입력")
menu_name = st.text_input("메뉴 이름", placeholder="예: 김치찌개")
member_name = st.selectbox("먹은 사람", df["ename"])
#member_name = st.text_input("먹은 사람", value="jiwon")
dt = st.date_input("먹은 날짜")

isPress = st.button("메뉴 저장")

if isPress:
    if menu_name and member_name and dt:
        if insert_menu(menu_name, member_name, dt):
            st.success(f"입력 성공")
        else:
            st.error(f"입력 실패")
    else:
        st.warning(f"모든 값을 입력해주세요!")


st.subheader("확인")
query =" SELECT menu_name, member_name, dt FROM lunch_menu ORDER BY dt DESC;"

conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()

#conn.commit()
cursor.close()
conn.close()

#selected_df = pd.DataFrame([[1,2,3]], columns=['a','b','c'])
selected_df = pd.DataFrame(rows, columns=['menu_name','member_name','dt'])
selected_df


st.subheader("통계")
#df = pd.read_csv('note/menu.csv')

#start_idx = df.columns.get_loc('2025-01-07')
#rdf= df.melt(id_vars=['ename'], value_vars=(df.columns[start_idx:-2]),var_name='dt', value_name='menu')
#not_na_rdf = rdf[~rdf['menu'].isin(['-','<결석>','x'])]
#gdf = not_na_rdf.groupby('ename')['menu'].count().reset_index()

not_na_rdf = selected_df[~selected_df['menu_name'].isin(['-','<결석>','x'])]
gdf = not_na_rdf.groupby('member_name')['menu_name'].count().reset_index()
gdf

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
    df = pd.read_csv('note/menu.csv')
    start_idx = df.columns.get_loc('2025-01-07')
    rdf= df.melt(id_vars=['ename'], value_vars=(df.columns[start_idx:-2]),var_name='dt', value_name='menu')
    not_na_rdf = rdf[~rdf['menu'].isin(['-','<결석>','x'])]
    
    for _, row  in not_na_rdf.iterrows():
        insert_menu(row['menu'], row['ename'], row['dt'])
    st.success(f"벌크 인서트 완료")


