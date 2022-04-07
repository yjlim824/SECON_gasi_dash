from django.shortcuts import render, redirect
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import pymysql
from ..models import Weather , Distance

def secon(request):

    # 전일 방문객 -> 대구달성 값으로 완료
    df = pd.read_csv('./data/DeviceCountDay.csv')
    df['time'] = pd.to_datetime(df['time']).dt.date
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    now = datetime.today()  # 현재 시간
    yesterday = (now - timedelta(days=40)).strftime('%Y-%m-%d')  # 어제 날짜, 시간값 삭제 임시로 날짜 설정
    df = df[df['time'] == yesterday]
    data = df.iloc[2][2]  # 전체값 지정
    # deltas = df.iloc[-2][:-1].sum()
    fig1 = go.Figure()
    fig1.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "전일 방문객", 'font': {'size': 15, 'color': '#C5C5C5'}},
            number={'suffix': '명', 'font': {'size': 20, 'color': '#ffffff'}, 'valueformat': ',.0f'},
            # delta=dict(reference=deltas, increasing=dict(color='blue'))
        )
    )
    fig1.update_layout(  # width=290,  # 데이터를 가운데로 맞추기 위해 넓이 없앰
        height=70,
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="rgba(0,0,0,0)")  # 텍스트상자배경색
    plot_div1 = plot(fig1, output_type='div')

    # 이번달 총 방문객 -> 대구달성 값으로 완료
    df = pd.read_csv('./data/DeviceCountMonthly.csv')
    data = df['data'][2]  # 이번달 지역 전체 총 방문객
    fig2 = go.Figure()
    fig2.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "이번달 총 방문객", 'font': {'size': 15, 'color': '#C5C5C5'}},
            number={'suffix': '명', 'font': {'size': 20, 'color': '#FFFFFF'}, 'valueformat': ',d'},
        )
    )
    fig2.update_layout(  # width=290,
        height=70,
        paper_bgcolor="rgba(0,0,0,0)")
    plot_div2 = plot(fig2, output_type='div')

    # 체류 시간 -> 대구달성 값으로 완료
    df = pd.read_csv('./data/DeviceResidenceTime.csv')
    df = df[df['zone'] == '전체']
    df['time'] = pd.to_datetime(df['time']).dt.date
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    now = datetime.today()
    yesterday = (now - timedelta(days=40)).strftime('%Y-%m-%d')  # 임시로 날짜 설정
    df = df[df['time'] == yesterday]
    data = df['data'].iloc[0]
    data = data // 100
    data
    fig3 = go.Figure()
    fig3.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "<b>체류 시간</b>", 'font': {'size': 15, 'color': '#C5C5C5'}},
            number={'prefix': '<b>', 'suffix': '분</b>', 'font': {'size': 20, 'family': "Arial", 'color': '#FFFFFF'},
                    'valueformat': 'd'},
        )
    )
    fig3.update_layout(  # width=290,
        height=70,
        paper_bgcolor="rgba(0,0,0,0)")
    plot_div3 = plot(fig3, output_type='div')

    # 지난주 재방문객 -> 대구달성 값으로 완료
    df = pd.read_csv('./data/DeviceCountRevisit.csv')
    df = df[df['zone'] == '전체']
    df['time'] = pd.to_datetime(df['time']).dt.date
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    data = df['data'].iloc[-7:].sum()
    fig4 = go.Figure()
    fig4.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "지난주 재방문객", 'font': {'size': 15, 'color': '#C5C5C5'}},
            number={'suffix': '명', 'font': {'size': 20, 'color': '#FFFFFF'}, 'valueformat': ',d'},
        )
    )
    fig4.update_layout(  # width=290,
        height=70,
        paper_bgcolor="rgba(0,0,0,0)")
    plot_div4 = plot(fig4, output_type='div')

    # 지역별 일일방문객 -> 대구달성 값으로 완료
    df = pd.read_csv('./data/DeviceCountDay.csv')
    zoneDay = go.Figure()
    region = df[df['zone'] != '전체']  # 전체 값을 빼고 데이터 프레임 만듦
    y = ['R&D    <br>연구시설 ', '미래형  <br>자동차  ', '주거단지 ']
    x = region['data']
    zoneDay.add_trace(
        go.Bar(
            y=y,
            x=x,
            text=x,
            orientation='h',
        )
    )
    zoneDay.update_traces(marker_color=['rgba(123,104,238,0.7)', 'rgba(137,176,255,0.7)', 'rgba(164,224,254,0.7)'],
                          marker_line_color='#ffffff',
                          marker_line_width=0.7, opacity=1, textposition='inside',
                          textfont_size=9, textfont_color="#ffffff")
    zoneDay.update_layout(
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
    plot_zoneDay = plot(zoneDay, output_type='div')

    # 지난요일별 방문객 -> 대구달성 값으로 완료
    df_lastw = pd.read_csv('./data/DeviceCountDay.csv')
    # del df_lastw['Unnamed: 0']
    now = datetime.today()
    weektoday = datetime.today().weekday()  # 오늘 요일구하기(0-월 6-일)

    df_lastw = df_lastw[df_lastw['zone'] == '전체']
    df_lastw['time'] = pd.to_datetime(df_lastw['time']).dt.date
    df_lastw['time'] = pd.to_datetime(df_lastw['time'], errors='coerce')

    startDate = now - timedelta(now.weekday()) - timedelta(8)  # 지난주 월요일 값을 구함
    # startDate =startDate.strftime('%Y-%m-%d')
    startDate = '2022-02-21'  # 임시값
    # endDate = now - timedelta(now.weekday())-timedelta(1) #지난주 일요일 값 구함
    endDate = '2022-02-27'  # 임시값
    df_lastw = df_lastw[(df_lastw['time'] >= startDate) & (df_lastw['time'] < endDate)]

    y = df_lastw['data']
    x = ['월', '화', '수', '목', '금', '토', '일']

    fig_w = go.Figure()
    fig_w.add_trace(
        go.Scatter(
            x=x,
            y=y,
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
        font=dict(color="#ffffff", size=9,)
    )
    plot_fig_w = plot(fig_w, output_type='div')



    # 지역별 지난주 재방문객 -> 대구달성 값으로 완료
    df = pd.read_csv('./data/DeviceCountRevisit.csv')
    fig_lastWeek = go.Figure()
    df = df[df['zone'] != '전체']
    df['time'] = pd.to_datetime(df['time']).dt.date
    df['time'] = pd.to_datetime(df['time'], errors='coerce')  # time열을 str 값으로 변환
    dfw = df[
        (df['time'] >= startDate) & (df['time'] < endDate)]  # 지난 일주일로만 데이터 프레임 만듦 startDate,endDate는 지난주 재방문객에서 선언함
    df1 = dfw[dfw['zone'] == 'R&D 연구시설단지']  # 연구시설단지 data 값만 더함
    sum1 = df1['data'].sum()
    df2 = dfw[dfw['zone'] == '미래형자동차']  # 미래형자동차 data 값만 더함
    sum2 = df2['data'].sum()
    df3 = dfw[dfw['zone'] == '주거단지']  # 주거단지 data 값만 더함
    sum3 = df3['data'].sum()
    x = ['R&D 연구시설단지', '미래형자동차', '주거단지']
    y = [sum1, sum2, sum3]
    fig_lastWeek.add_trace(
        go.Bar(
            y=y,
            x=x,
            text=y,
        )
    )
    fig_lastWeek.update_traces(marker_color=['rgba(123,104,238,0.7)', 'rgba(137,176,255,0.7)', 'rgba(164,224,254,0.7)'],
                               marker_line_color='#ffffff',
                               marker_line_width=0.7, opacity=1, textposition='inside',
                               textfont_size=14, textfont_color="#ffffff")
    fig_lastWeek.update_layout(  # width=500,
        height=300,
        xaxis=dict(autorange=True),
        yaxis=dict(visible=True),
        margin=dict(l=0, r=0, t=20, b=0),
        paper_bgcolor="#001B50",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        font=dict(color="#ffffff")
    )
    plot_lastWeek = plot(fig_lastWeek, output_type='div')

    # 환경센서 테이블

    df = pd.read_csv('./data/SensorDataHourlyDay.csv')
    del df_lastw['Unnamed: 0']
    df['time'] = pd.to_datetime(df['time']).dt.date
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df_sensor = df[['zone', 'dust', 'superdust', 'tvoc', 'temp', 'humid']]
    df_sensor = df_sensor[-5:]  # 최신 환경센서 데이터만 들고옴
    df_sensor = df_sensor[
        (df_sensor['zone'] == '주거단지') | (df_sensor['zone'] == '미래형 자동차1') | (df_sensor['zone'] == 'R&D 연구시설단지')]
    # df_sensor = df_sensor.set_index('zone')
    # df_sensor = df_sensor.style.hide_index()
    fig_sensor = go.Figure(data=[go.Table(
        columnwidth=[550, 300],
        header=dict(values=['', '<b>미세먼지</b><br>(&#181;g/m&#179;)', '<b>초미세먼지</b><br>(&#181;g/m&#179;)',
                            '<b>tvoc</b><br>(ppb)', '<b>온도</b><br>(&#8451;)', '<b>습도</b><br>(%)', ],
                    fill_color='rgba(0,0,0,0)',
                    line_color='rgba(0,0,0,0)',
                    align='center',
                    height=40,
                    font=dict(color='white', size=15)
                    ),
        cells=dict(values=[df_sensor.zone, df_sensor.dust, df_sensor.superdust, df_sensor.tvoc, df_sensor.temp,
                           df_sensor.humid],
                   fill_color='rgba(0,0,0,0)',
                   line_color='rgba(0,0,0,0)',
                   align='center',
                   height=40,
                   font=dict(color='white', size=14)
                   ))
    ])
    fig_sensor.update_layout(height=260,
                             margin=dict(l=0, r=0, t=0, b=0),
                             paper_bgcolor="#001B50",
                             plot_bgcolor="rgba(0,0,0,0)",
                             autosize=True,
                             )

    plot_sensor = plot(fig_sensor, output_type='div')

    # 미세먼지
    region_dust = df_sensor['dust'].iloc[0]  # 주거단지 미세먼지

    # 초미세먼지
    region_superdust = df_sensor['superdust'].iloc[0]  # 주거단지

    # tvoc
    region_tvoc = df_sensor['tvoc'].iloc[0]  # 주거단지

    # temp
    region_temp = df_sensor['temp'].iloc[0]  # 주거단지

    # humid
    region_humid = df_sensor['humid'].iloc[0]  # 주거단지


    # model
    weather = Weather()
    weather.temperature = region_temp
    weather.dust = region_dust
    weather.superdust = region_superdust
    weather.humid = region_humid
    weather.tvoc = region_tvoc
    weather.save()

    # 서버값 불러오기- 회사 데이터 쌓이는 것
    conn = pymysql.connect(host='172.30.1.220', user='gasi', password='gasi1234!', database='TSG_DB', port=3306,
                           charset='utf8')
    sql = 'SELECT * FROM TSG_DB.TSG_TE_DEVICE_SCAN_DATA_WIFI WHERE MAC = 88205820257752 ORDER BY `TIME` DESC '
    df = pd.read_sql(sql, conn)


    # 거리별 인원수
    people = [10, 30, 5] # 인원수 임의의 값 넣어줌
    distance = Distance()
    distance.long = people[1]
    distance.middle = people[0]
    distance.short = people[2]

    # 실시간 방문객 -> 대구달성 값으로 완료
    df_visitor = pd.read_csv('./data/DeviceCountHourly.csv')
    current_visitor = df_visitor[df_visitor['zone'] != '전체']
    colors = []
    for i in people:
        if i < 7:
            colors.append('rgba(137,176,255,0.85)')
        elif i < 20:
            colors.append('rgba(250,144,144,0.85)')
        elif i >= 20:
            colors.append('rgba(244,212,132,0.85)')

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
        height=270,
        annotations=[dict(text='<b>실시간<br>방문객</b>', font_size=11, showarrow=False)],
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        font=dict(color="#ffffff"),
        # showlegend=False,

    )
    plot_fig_pie = plot(fig_pie, output_type='div')

    return render(request, "dash/secon.html", context={'plot_div1': plot_div1,
                                                       'plot_div2': plot_div2,
                                                       'plot_div3': plot_div3,
                                                       'plot_div4': plot_div4,
                                                       'plot_div5': plot_zoneDay,
                                                       'plot_div6': plot_fig_w,
                                                       'plot_pie': plot_fig_pie,
                                                       'plot_div8': plot_lastWeek,
                                                       'plot_sensor': plot_sensor,
                                                       'region_dust': region_dust,
                                                       'region_superdust': region_superdust,
                                                       'region_tvoc': region_tvoc,
                                                       'region_temp': region_temp,
                                                       'region_humid': region_humid,
                                                       'weather': weather,
                                                       'distance': distance,
                                                       }
                  )


