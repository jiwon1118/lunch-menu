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
    ep = "https://raw.githubusercontent.com/jiwon1118/lunch-menu/refs/heads/main/endpoints.json"
    res = requests.get(ep)
    data = res.json()
    endpoints = data['endpoints']

    jiwon_url = None 
    urls = []
    results = []
    all_results = []
# URL 중 jiwon빼고 목록을 순회하면서 jiwon url의 df랑 비교하며 없는것을 데이터프레임으로 만들기
    for p in endpoints:
        if p['name'] == 'jiwon':
            jiwon_url = p['url']
        else:
            urls.append(p['url'])
    
    res = requests.get(jiwon_url)
    data_j = res.json()
    df_jiwon = pd.DataFrame(data_j)

    for url in urls:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            df_other = pd.DataFrame(data)   
        
            # _merge가 left_only 인것만 남기고 _merge column은 지우기
            diff_df = df_other.merge(df_jiwon, how='left', indicator=True)
            diff_df = diff_df[diff_df['_merge'] == 'left_only'].drop(columns=['_merge'])
        
            # 결과 데이터프레임을 저장합니다.
            results.append((url, diff_df))
    
# 데이터 프레임을 순회 하면서 insert 하기
    all_results = pd.concat([result for _, result in results], ignore_index=True)
    # print(combined_results)
    

    st.success(f"잔업완료 - 새로운 원천 {len(urls)}곳에서 총 {len(all_results)}건을 새로 추가 하였습니다.")
    print(f"확인 : {all_results}")
    
    st.subheader("확인")
    result_df = all_results
    result_df

