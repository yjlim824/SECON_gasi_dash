from django.shortcuts import render, redirect
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import pymysql
from ..models import Weather, Distance

def secon(request):

    # 현재 방문객
    df = pd.read_json('http://222.108.138.7:38888/v1/SECON/DeviceCountMin')
    df = df[df['data'] != 0]
    data = df['data'].iloc[0]
    currentVisitor = data

    # 체류 시간
    df = pd.read_json('http://222.108.138.7:38888/v1/TEST/DeviceResidenceTime')
    data = df['data'].iloc[0]
    data = data // 100
    periodVisitor = data


    # 오늘 총 방문객
    df = pd.read_json('http://222.108.138.7:38888/v1/SECON/DeviceCountHourly')
    data = df['data'].sum()
    dataTodayAll = data

    # 총 누적 방문객 -> 확인해보기
    df = pd.read_json('http://222.108.138.7:38888/v1/SECON/DeviceCountDay?from=2022-04-11&to=2022-04-16')
    data = df['data'].sum() + dataTodayAll
    allVisitor = data

    # 일별 방문객
    df = pd.read_json('http://222.108.138.7:38888/v1/SECON/DeviceCountDay?from=2022-04-14&to=2022-04-18')

    todayVisitor = go.Figure()
    df['time'] = pd.to_datetime(df['time']).dt.date
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df = df[(df['time'] >= '2022-04-14') & (df['time'] <= '2022-04-18')]
    x = df['data'].to_numpy()
    x = x.tolist()


    n = 3 - len(x)

    for i in range(n):
        x.append(0)

    y = ['4-14', '4-15', '4-16']
    todayVisitor.add_trace(
        go.Bar(
            y=y,
            x=x,
            text=x,
            orientation='h',
        )
    )
    todayVisitor.update_traces(marker_color=['rgba(123,104,238,0.7)', 'rgba(137,176,255,0.7)', 'rgba(164,224,254,0.7)'],
                               marker_line_color='#ffffff',
                               marker_line_width=0.7, opacity=1, textposition='inside',
                               textfont_size=9, textfont_color="#ffffff"
                               )
    todayVisitor.update_layout(
        width=180,
        height=120,
        xaxis=dict(autorange=True, zeroline=False),  # 그래프의 그리드와 영점선 삭제
        yaxis=dict(visible=True),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",  # 그래프 배경 투명색
        autosize=True,
        font=dict(color="#ffffff", size=9, )  # 그래프 폰트 색상 변경
    )
    plot_todayVisitor = plot(todayVisitor, output_type='div')

    # 대기 그래프
    df = pd.read_json('http://15.164.94.113:8000/v1/Gasi/SensorDataDayAverage')
    df['time'] = pd.to_datetime(df['time']).dt.hour
    df = df[(df['time'] >= 9) & (df['time'] <= 17)]
    y = df['temperature']
    x = df['time']
    fig_t = go.Figure()
    fig_t.add_trace(
        go.Scatter(
            x=x,
            y=y,
            line=dict(color='#FA9090'),
            name='온도',
            mode='markers + lines'))
    fig_t.add_trace(
        go.Scatter(
            x=x,
            y=df['humidity'],
            line=dict(color='#A4E0FE'),
            name='습도',
            mode='markers + lines'))

    fig_t.update_layout(
        width=350,
        height=120,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        font=dict(color="#ffffff", size=9,)
    )
    fig_t.update_yaxes(range=[10, 30])
    plot_fig_t = plot(fig_t, output_type='div')

    #미세먼지 초미세먼지
    fig_d = go.Figure()
    fig_d.add_trace(
        go.Scatter(
            x=x,
            y=df['pm10'],
            line=dict(color='#F6D787'),
            name='미세먼지',
            mode='markers + lines'))
    fig_d.add_trace(
        go.Scatter(
            x=x,
            y=df['pm2_5'],
            line=dict(color='#84EA7C'),
            name='초미세먼지',
            mode='markers + lines'))

    fig_d.update_layout(
        width=350,
        height=120,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        font=dict(color="#ffffff", size=9, )
    )
    fig_d.update_yaxes(range=[0, 20])
    plot_fig_d = plot(fig_d, output_type='div')

    # tvoc
    fig_tvoc = go.Figure()
    fig_tvoc.add_trace(
        go.Scatter(
            x=x,
            y=df['tvoc'],
            line=dict(color='#FF62DC'),
            name='tvoc',
            mode='markers + lines'))

    fig_tvoc.update_layout(
        width=350,
        height=120,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        font=dict(color="#ffffff", size=9, )
    )
    #fig_tvoc.update_yaxes(range=[0, 20])
    plot_fig_tvoc = plot(fig_tvoc, output_type='div')

    # 시간별 그래프
    df_time = pd.read_json('http://222.108.138.7:38888/v1/SECON/DeviceCountHourly')

    df_time['time'] = pd.to_datetime(df_time['time']).dt.hour

    df_time = df_time[(df_time['time'] >= 9) & (df_time['time'] <= 17)]

    y1 = df_time['data'].to_numpy()
    y1 = y1.tolist()
    y1.reverse()

    n = 9 - len(y1)
    for i in range(n):
        y1.append(0)

    x1 = ['9', '10', '11', '12', '13', '14', '15', '16', '17']

    fig_w = go.Figure()
    fig_w.add_trace(
        go.Scatter(
            x=x1,
            y=y1,
            line=dict(color='#FFAB7C'),
            mode='markers + lines'))

    fig_w.update_layout(
        width=180,
        height=120,
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        font=dict(color="#ffffff", size=9, )
    )
    plot_fig_w = plot(fig_w, output_type='div')



    # 환경센서 테이블

    df = pd.read_json('http://222.108.138.7:38888/v1/TEST/SensorDataHourly')
    df['time'] = pd.to_datetime(df['time']).dt.date
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df_sensor = df[['temperature', 'humidity', 'pm10', 'pm2_5', 'tvoc']]

    # 미세먼지
    region_dust = df_sensor['pm10'].iloc[0]  # 주거단지 미세먼지

    # 초미세먼지
    region_superdust = df_sensor['pm2_5'].iloc[0]  # 주거단지

    # tvoc
    region_tvoc = df_sensor['tvoc'].iloc[0]  # 주거단지

    # temp
    region_temp = df_sensor['temperature'].iloc[0]  # 주거단지

    # humid
    region_humid = df_sensor['humidity'].iloc[0]  # 주거단지


    # model
    weather = Weather()
    weather.temperature = region_temp
    weather.dust = region_dust
    weather.superdust = region_superdust
    weather.humid = region_humid
    weather.tvoc = region_tvoc
    weather.save()

    # 서버값 불러오기- 회사 데이터 쌓이는 것
    #conn = pymysql.connect(host='172.30.1.220', user='gasi', password='gasi1234!', database='TSG_DB', port=3306, charset='utf8')
    #sql = 'SELECT * FROM TSG_DB.TSG_TE_DEVICE_SCAN_DATA_WIFI WHERE MAC = 88205820257752 ORDER BY `TIME` DESC '
    #df = pd.read_sql(sql, conn)


    # 재방문객 수

    people = [10, 30, 3] # 인원수 임의의 값 넣어줌
    distance = Distance()
    distance.long = people[1]
    distance.middle = people[0]
    distance.short = currentVisitor #현재 방문객

    # 방문객 혼잡도
    df_visitor = pd.read_csv('./data/DeviceCountHourly.csv')
    current_visitor = df_visitor[df_visitor['zone'] != '전체']
    colors = []
    for i in people:
        if i < 7:
            colors.append('rgba(137,176,255,0.85)')
        elif i < 20:
            colors.append('rgba(244,212,132,0.85)')
        elif i >= 20:
            colors.append('rgba(250,144,144,0.85)')

    fig_pie = go.Figure()
    fig_pie.add_trace(
        go.Pie(labels=['10m', '15m', '5m'],
               values=people,
               textinfo='percent',
               insidetextorientation='tangential',
               marker_colors=colors,
               marker_line_color='#ffffff',
               marker_line_width=1.5,
               textfont_size=10,
               textfont_color="#ffffff",
               hole=0.4)
    )
    fig_pie.update_layout(  # width=500,  # 원형그래프가 상자 안에 들어 올 수 있게 크기 조정
        height=240,
        annotations=[dict(text='<b>실시간<br>방문객</b>', font_size=11, showarrow=False)],
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        font=dict(color="#ffffff"),
        # showlegend=False,

    )
    plot_fig_pie = plot(fig_pie, output_type='div')

    #test = pd.read_json('http://172.30.1.220:8000/v1/TEST/DeviceCountDay')
    #a = test['data']



    return render(request, "dash/secon.html", context={'currentVisitor': currentVisitor,
                                                       'allVisitor': allVisitor,
                                                       'periodVisitor': periodVisitor,
                                                       'dataTodayAll': dataTodayAll,
                                                       'plot_todayVisitor': plot_todayVisitor,
                                                       'plot_div6': plot_fig_w,
                                                       'plot_t': plot_fig_t,
                                                       'plot_d': plot_fig_d,
                                                       'plot_tvoc': plot_fig_tvoc,
                                                       'plot_pie': plot_fig_pie,
                                                       'region_dust': region_dust,
                                                       'region_superdust': region_superdust,
                                                       'region_tvoc': region_tvoc,
                                                       'region_temp': region_temp,
                                                       'region_humid': region_humid,
                                                       'weather': weather,
                                                       'distance': distance,
                                                       }
                  )


