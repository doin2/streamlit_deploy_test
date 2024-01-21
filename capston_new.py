import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd 
import folium
import time 

from streamlit_folium import folium_static
from sklearn.preprocessing import MinMaxScaler

import time 

with st.spinner('인구데이터 불러오는 중...'):
  time.sleep(5)
  st.success('완료') 

# st.markdown("""
# <style>
# .reportview-container .main {
#     max-width: 80%;
# }
# </style>
# """, unsafe_allow_html=True)

# st.set_page_config(layout="wide")



st.sidebar.title('년도 및 지역 선택')
select_year = st.sidebar.selectbox('년도 선택',['2018','2019','2020','2021','2022'])
select_area = st.sidebar.selectbox('지역선택'
                                              ,['서울특별시','부산광역시','대구광역시','인천광역시','광주광역시','대전광역시','울산광역시','세종특별자치시','경기도','강원특별자치도','충청북도','충청남도','전라북도','전라남도','경상북도','경상남도','제주특별자치도']
                                              )
select_area_text = select_area[0]


sall = {'region':['서울특별시', '부산광역시', '대구광역시', '인천광역시','광주광역시','대전광역시', '울산광역시','세종특별자치시','경기도','강원특별자치도','충청북도','전라북도','전라남도', '경상북도','경상남도','제주특별자치도'],
        '위도':[37.5635694444444, 35.17701944, 35.86854167, 37.45323333, 35.156975, 36.34711944, 35.53540833, 36.4800121, 35.23473611, 38.642618, 36.6325, 35.81727, 34.81304444, 36.491286, 35.459369, 33.48569444],
       '경도':[126.980008333333, 129.0769528, 128.6035528, 126.7073528, 126.8533639, 127.3865667, 129.3136889, 127.2890691, 128.6941667, 127.170231, 127.4935861, 127.1110528, 126.465, 128.889433, 128.214826, 126.5003333]}

select_area_location = pd.DataFrame(sall)

select_area_location_latitude = select_area_location[select_area_location['region'] == select_area]['위도'].values
select_area_location_latitude_value = select_area_location_latitude[0]

select_area_location_hardness = select_area_location[select_area_location['region'] == select_area]['경도'].values
select_area_location_hardness_value = select_area_location_hardness[0]


# if select_year=='2022': #파일 선택하는것
#     selected_year=

#___________________________________________________________________________________________________


geo_json = 'https://raw.githubusercontent.com/vuski/admdongkor/master/ver20221001/HangJeongDong_ver20221001.geojson'

#uploaded = files.upload()

# 파일 업로드 후 
# data_h1 = pd.read_csv(f'C:\\Users\\82105\\Desktop\\2023_05_26_capstone_1\\{select_year}_{select_area_text}_완료.csv')
data_h1 = pd.read_csv(f'C:\\Users\\82105\\Desktop\\2023_05_26_capstone_1\\정제 완료 데이터\\{select_year}완료지역.csv')

data_h2 = pd.read_csv(f'C:\\Users\\82105\\Desktop\\2023_05_26_capstone_1\\정제 완료 데이터\\{select_year}완료지역.csv')

select_area_chosen = data_h1[data_h1['지역'] == select_area]

#___________________________________________________________________________________________________

# df = px.data.gapminder()
# fig = px.scatter(
#     df.query("year==2007"),
#     x="gdpPercap",
#     y="lifeExp",
#     size="pop",
#     color="continent",
#     hover_name="country",
#     log_x=True,
#     size_max=60,
# )
# df
#____________________________________________________________________

dfs = select_area_chosen.sort_values('총인구수')
dfs = dfs.iloc[:-20]
dfs = dfs.reset_index(drop=True)

# DataFrame 'dfs'의 행 순서를 랜덤하게 섞기
# dfran = data_h1.sample(frac=1).reset_index(drop=True)

# '구간별_데이터_개수'
# '조출생률'
# dfran.index

fig = px.scatter(
    dfs,
    x=dfs.index,
    y='조출생률',
    size="총인구수",
    color="지역",
    # hover_name="country",

    # size_max=30,
)
fig.update_traces(marker=dict(line=dict(width=0)))


# fig.show()

dfs2 = data_h2.sort_values('총인구수')
dfs2 = dfs2.iloc[:-20]
dfs2 = dfs2.reset_index(drop=True)


#___________________________________________________________________________________________________
fig2 = px.scatter(
    dfs2,
    x=dfs2.index,
    y='조출생률',
    size="총인구수",
    color="지역",
    # hover_name="country",

    # size_max=30,
)
fig2.update_traces(marker=dict(line=dict(width=0)))
fig2.update_layout(title_text=f'{select_year}년 전국 출생 데이터',width=800, height=400)

st.plotly_chart(fig2, theme="streamlit")#플롯리 차트
#___________________________________________________________________________________________________

# select_area_chosen_pop = select_area_chosen['총인구수'][0]

tab1, tab2 = st.tabs(["선택한 구역별", "전국"])



col1, col2, col3 = st.columns(3)
with col2:
    with tab1:
        # st.subheader(f'{select_area} 인구 : {select_area_chosen_pop}')  

        


        #___________________________________________________________________________________________________
        mean_values = select_area_chosen["조출생률"].mean()
        median_values = select_area_chosen["조출생률"].median()
        all_mean = data_h1["조출생률"].mean()
        all_median = data_h1["조출생률"].median()

        mdf = pd.DataFrame({
            '값': [mean_values, median_values],
            '구분': ['평균', '중간값']
        })

        fig2 = px.bar(data_frame=mdf,
                    x="값",
                    y="구분",
                    orientation='h')

        # X 축 범위 설정: 1부터 최대값까지 
        fig2.update_layout(title_text=f'{select_area} 출산율 평균, 중간값',
                        xaxis_range=[(mdf['값'].min() - 0.5), mdf['값'].max()], height=200)
        fig2.update_traces(marker_color='green')

        st.plotly_chart(fig2)
        #___________________________________________________________________________________________________


        #___________________________________________________________________________________________________
        st.subheader(f'{select_area} 츨산율 지도') 
        
        m = folium.Map(
        # 위도, 경도 
        location=[select_area_location_latitude_value,select_area_location_hardness_value], #좌표 수정필요
        # 시각화 스타일
        tiles='cartodbpositron',     width='100%',height='100%'
    )
        # choropleth = 
        folium.Choropleth(
        geo_data=geo_json,
        name ='choropleth', #별거아님 레이어설정
        data = select_area_chosen,   #경계 데이터 지정 geo_json에서 가져온거
        columns=['loc','조출생률'],  #csv파일에서 가져오는것 첫번째는 위치정보 loc는 위치정보 두번쨰열은 조출생률 열 선택
        key_on='feature.properties.adm_cd2', #GeoJSON 파일과 데이터프레임 연결하는것
        fill_color='RdPu', # 색깔
        width=900, 
        height=600,
        #투명도 
        nan_fill_color='white',  # 배경색과 동일하게 설정
        nan_fill_opacity=0,
        fill_opacity=0.9, # 색 투명도
        line_opacity=0.1  # 경계선 굵기
        
    ).add_to(m)
        
        # # GeoJson layer for the tooltip 마우스 갖다대면 지역명 표시
        # tooltip_layer = folium.GeoJson(
        #     geo_json,
        #     name="Tooltip Layer",
        #     style_function=lambda x: {'color':'transparent','fillColor':'transparent','weight':0},
        #     tooltip=folium.features.GeoJsonTooltip(fields=['adm_nm'], aliases=[''])
        # )
        # tooltip_layer.add_to(choropleth.geojson)
        
        # data_h1
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.

        folium_static(m)        
        #___________________________________________________________________________________________________
        




#___________________________________________________________________________________________________  


    with tab2:
            
            mdf2 = pd.DataFrame({
                '값': [all_mean, all_median],
                '구분': ['평균', '중간값']
            })

            fig3 = px.bar(data_frame=mdf2,
                        x="값",
                        y="구분",
                        orientation='h')

            # X 축 범위 설정: 1부터 최대값까지 
            fig3.update_layout(title_text='전국 출산율 평균, 중간값',
                            xaxis_range=[(mdf2['값'].min() - 0.5), mdf2['값'].max()], height=200)

            # st.plotly_chart(fig3)            
            #___________________________________________________________________________________________________
            

            # Use the native Plotly theme.
            # st.plotly_chart(fig, theme=None, use_container_width=True)
            st.plotly_chart(fig3)

            st.sidebar.title(' ')



            # 평균과 중앙값 계산
            # mean_values = data_h1["조출생률"].mean()
            # median_values = data_h1["조출생률"].median()
            all_mean = data_h1["조출생률"].mean()
            all_median = data_h1["조출생률"].median()

            mdf = pd.DataFrame({
                '값': [mean_values, all_mean,median_values, all_median],
                '구분': ['평균', '전국평균', '중간값', '전국중간값']
            })

            fig4 = px.bar(data_frame=mdf,
                        x="값",
                        y="구분",
                        orientation='h')


            #___________________________________________________________________________________________________



            m = folium.Map(
            # 위도, 경도 
            location=[36.684273, 128.068635], #좌표 수정필요
            zoom_start=6.5, width="100%", height="100%",
            # 시각화 스타일
            tiles='cartodbpositron',
        )
            # choropleth = 
            folium.Choropleth(
            geo_data=geo_json,
            name ='choropleth', #별거아님 레이어설정
            data = data_h1,   #경계 데이터 지정 geo_json에서 가져온거
            columns=['loc','조출생률'],  #csv파일에서 가져오는것 첫번째는 위치정보 loc는 위치정보 두번쨰열은 조출생률 열 선택
            key_on='feature.properties.adm_cd2', #GeoJSON 파일과 데이터프레임 연결하는것
            fill_color='RdPu', # 색깔
            # width=750, 
            # height=500,
            #투명도 
            nan_fill_color='white',  # 배경색과 동일하게 설정
            nan_fill_opacity=0,
            fill_opacity=0.9, # 색 투명도
            line_opacity=0.1  # 경계선 굵기
            
        ).add_to(m)


            st.subheader('전국 츨산율 지도')
            folium_static(m)
            #___________________________________________________________________________________________________



#--------------------------------------------------------------------------------------
