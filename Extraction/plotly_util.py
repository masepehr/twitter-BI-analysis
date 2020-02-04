import datetime
import pandas as pd
import plotly
import plotly.graph_objects as go


def plotly_scatter(x_data,y_data, color='green',
                   title=None,
                   xlabel=None,
                   ylabel=None,
                   height=300):
    data=[go.Scatter(x=x_data, y=y_data,
                mode='lines',
                opacity=0.8,
                marker_color=color)]

    html = plotly.offline.plot(
        {"data": data,
         "layout": go.Layout(barmode='overlay',
                             title=title,
                             yaxis_title=ylabel,
                             xaxis_title=xlabel,
                             height=height)},
        output_type="div",
        show_link=False)
    # fig = go.Figure(
    #     {"data": data,
    #      "layout": go.Layout(barmode='overlay',
    #                          title=title)})
    return html

def plotly_pie(x_label,
               y_data,
                   title=None,
                    width=300,height=300):
    data=[go.Pie(labels=list(sorted([int(a) for a in x_label])),sort=False, values=y_data,
                 textinfo='label+percent',
                                 insidetextorientation='radial',
                                 )]




    html = plotly.offline.plot(
        {"data": data,
         "layout": go.Layout(title=title)},
        output_type="div",
        show_link=False,include_plotlyjs=False)

    return html

def plotly_heatmap(tweets_df):
    year = datetime.datetime.now().year
    allday_tweet=tweets_df.set_index('date').groupby(pd.Grouper(freq='D')).count()['text']
    allday_tweet=allday_tweet.loc['2018-01-01':'2018-12-30']
    d1 = datetime.date(2018,1, 1)
    d2 = datetime.date(2018, 12, 30)

    delta = d2 - d1



     # gives me a list with datetimes for each day a year
    dates_in_year = [datetime.datetime.date(a) for a in allday_tweet.index] # gives me a list with datetimes for each day a year
    weekdays_in_year =[a for a in allday_tweet.index.dayofweek] # gives [0,1,2,3,4,5,6,0,1,2,3,4,5,6,…] (ticktext in xaxis dict translates this to weekdays
    weeknumber_of_dates = [i.strftime("%G-%V")[2:] for i in dates_in_year]  # gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,…] name is self-explanatory
    z = allday_tweet.loc['2018-01-01':'2018-12-30']
    text = [str(i) for i in dates_in_year]  # gives something like list of strings like ‘2018-01-25’ for each date. Used in data trace to make good hovertext.
    # 4cc417 green #347c17 dark green
    colorscale = [
        # Let first 10% (0.1) of the values have color rgb(0, 0, 0)
        [0.8, "rgb(0, 0, 0)"],
        [1.0, "rgb(0, 0, 0)"],



        [0.5, "rgb(60, 60, 60)"],
        [0.8, "rgb(60, 60, 60)"],



        [0, "rgb(100, 100, 100)"],
        [0.5, "rgb(100, 100, 100)"],


    ]
    data = [
        go.Heatmap(
            x=weeknumber_of_dates,
            y=weekdays_in_year,
            z=z,
            text=text,
            hoverinfo='text',
    xgap = 3,  # this
           ygap = 3,  # and this is used to make the grid-like apperance
                  showscale = False,
                              colorscale = colorscale
    )
    ]
    layout = go.Layout(
            title='activity chart',
            height =300,

             yaxis = dict(showline=False,
                showgrid=False,
                zeroline=False,
                tickmode='array',
                ticktext = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                tickvals = [0, 1, 2, 3, 4, 5, 6],),
            xaxis = dict(showline=False,
                         showgrid=False,
                         zeroline=False,),
             font = {'size':10, 'color':'#9e9e9e'},
             plot_bgcolor = ('#fff'),
             margin = dict(t=40),)

    fig = go.Figure(data=data, layout=layout)



    html = plotly.offline.plot(fig, auto_open=False, output_type='div')
    return html

    # app = dash.Dash()
    # app.layout = html.Div([
    #     dcc.Graph(id=‘heatmap - test’, figure = holidays(), config = {‘displayModeBar’: False})
    # ])
