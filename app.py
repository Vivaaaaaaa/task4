import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(layout="wide")
st.title('Steam User Data Dashboard')


# 加载数据
@st.cache_data
def load_data():
    file_path = 'steam-200k.csv'  # 修改为相对路径
    data = pd.read_csv(file_path, header=None)
    data.columns = ['UserID', 'Game', 'Action', 'Value', 'Unused']
    return data


try:
    data = load_data()

    # 拆分购买和游玩数据
    purchase_data = data[data['Action'] == 'purchase']
    play_data = data[data['Action'] == 'play']

    # 创建两列布局
    col1, col2 = st.columns(2)

    with col1:
        # 购买和游玩比例饼图
        purchase_count = len(purchase_data)
        play_count = len(play_data)

        pie_fig = go.Figure(data=[go.Pie(
            labels=['Purchase', 'Play'],
            values=[purchase_count, play_count],
            hole=0.3,
            pull=[0.1, 0]
        )])
        pie_fig.update_layout(title='User Actions Distribution')
        st.plotly_chart(pie_fig, use_container_width=True)

    with col2:
        # Top 15 最多游玩的游戏
        top_15_play = play_data['Game'].value_counts().head(15)
        play_fig = go.Figure(data=[go.Bar(
            x=top_15_play.values[::-1],
            y=top_15_play.index[::-1],
            orientation='h',
            marker_color='lightgreen'
        )])
        play_fig.update_layout(title='Top 15 Most Played Games')
        st.plotly_chart(play_fig, use_container_width=True)

    # 创建三列布局
    col3, col4, col5 = st.columns(3)

    with col3:
        # Top 15 购买次数最多的游戏
        top_15_purchase = purchase_data['Game'].value_counts().head(15)
        purchase_fig = go.Figure(data=[go.Bar(
            x=top_15_purchase.values[::-1],
            y=top_15_purchase.index[::-1],
            orientation='h',
            marker_color='skyblue'
        )])
        purchase_fig.update_layout(title='Top 15 Most Purchased Games')
        st.plotly_chart(purchase_fig, use_container_width=True)

    with col4:
        # 平均游玩时长
        playtime_avg = play_data.groupby('Game')['Value'].mean().sort_values(ascending=False).head(15)
        playtime_fig = go.Figure(data=[go.Bar(
            x=playtime_avg.values[::-1],
            y=playtime_avg.index[::-1],
            orientation='h',
            marker_color='salmon'
        )])
        playtime_fig.update_layout(title='Top 15 Games by Average Playtime')
        st.plotly_chart(playtime_fig, use_container_width=True)

    with col5:
        # 游戏粘度分析
        play_summary = play_data.groupby('Game')['Value'].sum()
        purchase_summary = purchase_data['Game'].value_counts()
        stickiness = play_summary / purchase_summary
        stickiness = stickiness.dropna().sort_values(ascending=False).head(15)

        stickiness_fig = go.Figure(data=[go.Bar(
            x=stickiness.values[::-1],
            y=stickiness.index[::-1],
            orientation='h',
            marker_color='pink'
        )])
        stickiness_fig.update_layout(title='Top 15 Games by Stickiness')
        st.plotly_chart(stickiness_fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")