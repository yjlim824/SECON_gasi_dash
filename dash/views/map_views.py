# 이 파일 수정시 서버를 재 시동해야함
from django.shortcuts import render, redirect
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def map(request):

    people = [20, 30, 10]

    colors = ['rgba(137,176,255,0.6)', 'rgba(172,217,71,0.6)', 'rgba(227,151,49,0.6)', 'rgba(236,40,40,0.6)', '#ffffff']
    color_order = []
    color1 = []
    color2 = []
    color3 = []

    for i in people:
        if i <= 5:
            color_order.append(colors[0])
        elif i <= 10:
            color_order.append(colors[1])
        elif i <= 20:
            color_order.append(colors[2])
        elif i > 20:
            color_order.append(colors[3])

    color1.append(color_order[0])
    color1.append(color_order[0])
    color2.append(color_order[1])
    color2.append(color_order[1])
    color3.append(color_order[2])
    color3.append(color_order[2])


    fig_pie = go.Figure()
    fig_pie.add_trace(
        go.Pie(labels=['60m', ''],
               values=[people[0], 0],
               #textinfo='percent',
               #insidetextorientation='tangential',
               marker_colors=color1,
               marker_line_color='rgba(0,0,0,0)',
               marker_line_width=1.5,
               textfont_size=14,
               textfont_color="rgba(0,0,0,0)",
               #hole=0.65
               )
    )
    fig_pie.update_traces(textinfo='none')
    fig_pie.update_layout(#width=500,  # 원형그래프가 상자 안에 들어 올 수 있게 크기 조정
                          height=300,
                          #annotations=[dict(text='실시간<br>유동인구', font_size=17, showarrow=False)],
                          margin=dict(l=0, r=0, t=0, b=0),
                          paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)",
                          autosize=True,
                          font=dict(color="rgba(0,0,0,0)"),
                          showlegend=False,
                          )
    circle1 = plot(fig_pie, output_type='div')


    fig_pie2 = go.Figure()
    fig_pie2.add_trace(
        go.Pie(labels=['40m', ''],
               values=[people[1], 0],
               textinfo='percent',
               insidetextorientation='tangential',
               marker_colors=color2,
               marker_line_color='rgba(0,0,0,0)',
               marker_line_width=1.5,
               textfont_size=14,
               textfont_color="rgba(0,0,0,0)",
               # hole=0.5
               )
    )
    fig_pie2.update_traces(textinfo='none')
    fig_pie2.update_layout(  # width=500,  # 원형그래프가 상자 안에 들어 올 수 있게 크기 조정
        height=200,
        # annotations=[dict(text='실시간<br>유동인구', font_size=17, showarrow=False)],
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        font=dict(color="rgba(0,0,0,0)"),
        showlegend=False,
    )
    circle2 = plot(fig_pie2, output_type='div')

    fig_pie3 = go.Figure()
    fig_pie3.add_trace(
        go.Pie(labels=['20m', ''],
               values=[people[2], 0],
               textinfo='percent',
               insidetextorientation='tangential',
               marker_colors=color3,
               marker_line_color='rgba(0,0,0,0)',
               marker_line_width=1.5,
               textfont_size=14,
               textfont_color="rgba(0,0,0,0)",
               # hole=0.5
               )
    )
    fig_pie3.update_traces(textinfo='none')
    fig_pie3.update_layout(  # width=500,  # 원형그래프가 상자 안에 들어 올 수 있게 크기 조정
        height=100,
        # annotations=[dict(text='실시간<br>유동인구', font_size=17, showarrow=False)],
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        font=dict(color="rgba(0,0,0,0)"),
        showlegend=False,
    )
    circle3 = plot(fig_pie3, output_type='div')
    people1 = people[0]
    people2 = people[1]
    people3 = people[2]




    return render(request, "dash/map.html", context={'circle1': circle1,
                                                     'circle2': circle2,
                                                     'circle3': circle3,
                                                     'people1': people1,
                                                     'people2': people2,
                                                     'people3': people3})
