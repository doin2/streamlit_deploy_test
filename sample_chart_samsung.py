import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

stock_data = yf.download('005930.KS', start='2020-01-01', end='2023-12-31')

buy_dates = pd.to_datetime(['2020/01/29', '2020/01/30', '2020/02/04', '2020/02/05', '2020/02/07', '2020/02/14',
                            '2020/02/17', '2020/02/25', '2020/03/02', '2020/08/12', '2020/09/04', '2020/09/11',
                            '2020/09/14', '2020/09/16', '2020/10/13', '2021/01/20', '2023/05/25'])
sell_dates = pd.to_datetime(['2020/01/02', '2020/01/30', '2020/02/07', '2020/02/17', '2020/03/02', '2020/03/03',
                             '2020/03/06', '2020/08/20', '2020/09/21', '2020/09/28', '2021/12/02', '2022/03/10'])

s = pd.to_datetime(["2022/07/13"])

trace = go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Stock Price')

buy_scatter = go.Scatter(x=[date for date in buy_dates if date in stock_data.index],
                         y=[stock_data.loc[date, 'Close'] for date in buy_dates if date in stock_data.index],
                         mode='markers', name='Buy', marker=dict(symbol='star-triangle-up', size=15, color='green'))

sell_scatter = go.Scatter(x=[date for date in sell_dates if date in stock_data.index],
                          y=[stock_data.loc[date, 'Close'] for date in sell_dates if date in stock_data.index],
                          mode='markers', name='Sell', marker=dict(symbol='circle', size=15, color='red'))

s2  = go.Scatter(x=[date for date in s if date in stock_data.index],
                          y=[90000],
                          mode='markers', name='Sell2', marker=dict(symbol='circle', size=15, color='red'))

data = [trace, buy_scatter, sell_scatter, s2]

layout = go.Layout(title='Stock Price with Buy & Sell Points', 
    yaxis=dict(title='Price'),
    # width=1800,  # 차트의 너비 설정
    # height=800  # 차트의 높이 설정
)
fig = go.Figure(data=data, layout=layout)

st.plotly_chart(fig)


#_________________________________________________________________________
# fig2 = go.Figure(data=stock_data, layout=layout)
# 캔들스틱 차트 생성
fig2 = go.Figure(data=[go.Candlestick(x=stock_data.index,
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Close'],
                increasing=dict(line=dict(color='blue', width=1)), 
                decreasing=dict(line=dict(color='yellow', width=1)))])

# 구매 및 판매 포인트를 차트에 표시
fig2.add_trace(go.Scatter(x=[date for date in buy_dates if date in stock_data.index],
                         y=[stock_data.loc[date, 'Close'] for date in buy_dates if date in stock_data.index],
                         mode='markers', name='Buy', marker=dict(symbol='triangle-up', size=10, color='green')))

fig2.add_trace(go.Scatter(x=[date for date in sell_dates if date in stock_data.index],
                         y=[stock_data.loc[date, 'Close'] for date in sell_dates if date in stock_data.index],
                         mode='markers', name='Sell', marker=dict(symbol='triangle-down', size=10, color='red')))

# 차트 레이아웃 설정
fig2.update_layout(title='Stock Price with Buy & Sell Points', yaxis_title='Price', width=1800, height=800)

# 스트림릿에 차트 그리기
st.plotly_chart(fig2)
