import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout="wide")


stock_data = yf.download('nvda', start='2024-05-01', end='2024-09-21')

buy_dates = pd.to_datetime(['2024/05/23', '2024/07/25', '2024/07/25', '2024/07/30', '2024/07/30', '2024/07/31',
                            '2024/08/02', '2024/08/05', '2024/08/08', '2024/09/04', '2024/09/04', '2024/09/05',
                            '2024/09/06'])
sell_dates = pd.to_datetime(['2024/06/05', '2024/07/31', '2024/08/20', '2024/08/20', '2024/08/20', '2024/08/22',
                             '2024/08/22', '2024/08/22', '2024/08/26', '2024/09/17', '2024/09/18', '2024/09/19'])

s = pd.to_datetime(["2022/07/13"])

trace = go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Stock Price')

buy_scatter = go.Scatter(x=[date for date in buy_dates if date in stock_data.index],
                         y=[stock_data.loc[date, 'Close'] for date in buy_dates if date in stock_data.index],
                         mode='markers', name='Buy', marker=dict(symbol='triangle-up', size=10, color='green'))

sell_scatter = go.Scatter(x=[date for date in sell_dates if date in stock_data.index],
                          y=[stock_data.loc[date, 'Close'] for date in sell_dates if date in stock_data.index],
                          mode='markers', name='Sell', marker=dict(symbol='triangle-up', size=10, color='red'))

s2  = go.Scatter(x=[date for date in s if date in stock_data.index],
                          y=[90000],
                          mode='markers', name='Sell2', marker=dict(symbol='triangle-up', size=10, color='red'))

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
                         mode='markers', name='Buy', marker=dict(symbol='triangle-up', size=5, color='green')))

fig2.add_trace(go.Scatter(x=[date for date in sell_dates if date in stock_data.index],
                         y=[stock_data.loc[date, 'Close'] for date in sell_dates if date in stock_data.index],
                         mode='markers', name='Sell', marker=dict(symbol='triangle-down', size=5, color='red')))

# 차트 레이아웃 설정
# fig2.update_layout(title='Stock Price with Buy & Sell Points', yaxis_title='Price', width=1800, height=800)

# 스트림릿에 차트 그리기
st.plotly_chart(fig2)
