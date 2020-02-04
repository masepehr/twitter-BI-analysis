from time import sleep
import pandas as pd
import requests
from django.core import files
from io import BytesIO

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError

from .plotly_util import plotly_scatter, plotly_pie,plotly_heatmap
from .utils import get_by_key,get_by_name
# Create your views here.
from django.views import View
from twdata.models import Persons,Tweets
from .analys import analys_person
# from bokeh.plotting import figure,output_file,show
# from bokeh.embed import components

from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go
import plotly.express as px
import calendar
from .info import get as getinfo


def load_from_db(username):
    persons = Persons.objects.filter(uname=username)
    if len(persons)>0:

        tweets = analys_person(persons[0])
        return tweets

    return None


def scrap_data(username):
    pass
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

class HomeView(View):
    def get(self,request):
        return render(request,template_name="Extraction/index2.html")

    def post(self,request):

        username=request.POST.get("seach_key")
        # load from cache
        # if not load from database
        tweets=load_from_db(username)
        if tweets is None:

        # if not request to api

            try:
                tweets = get_by_name(name=username, filename='tw.txt', proxy='127.0.0.1:39889', numtweet=100)


                #

                if len(tweets)>0:
                    # save in database
                    # analys
                    if tweets[0]==-1:
                        raise Exception
                    else:
                        print('sucess')
                        persons=Persons.objects.filter(uname=username)
                        if len(persons)==0:

                            person = Persons(uname=username)
                            person.save()
                        else:
                            person=persons[0]
                        for twit in tweets:

                            try:
                                tweet = Tweets(author=person,
                                               text=twit.text,
                                               date=twit.date,
                                               likes_count=twit.favorites,
                                               hashtags=twit.hashtags,
                                               replies_count=twit.replies,
                                               retweets_count=twit.retweets
                                               )
                                tweet.save()



                            except IntegrityError:
                                print('duplicaed')
                            except Exception as ex:
                                print(ex)


                        print('sucessfully')
                        # TODO: should fix problem
                        # fetch other info
                        name, tweets_num, following, followers, likes, date, pic, infs = getinfo(
                            "http://twitter.com/" + username)
                        # get pic

                        proxies = {"http": "http://127.0.0.1:39889", "https": "http:127.0.0.1:39889", }

                        resp = requests.get(pic, proxies=proxies)

                        if resp.status_code != requests.codes.ok:
                            file_name = 'unknown.png'
                        else:
                            fp = BytesIO()
                            fp.write(resp.content)
                            file_name = pic.split("/")[
                                -1]  # There's probably a better way of doing this but this is just a quick example
                        # your_model.image_field.save(file_name, files.File(fp))

                        person.followers = followers
                        person.followings = following
                        person.save()
                        if file_name != 'unknown.png':
                            person.pic.save(file_name, files.File(fp))
                        else:
                            person.pic.save(file_name)
                        person.save()
                else:
                    print('no tweet for this username')


            except Exception as TypeError:


                return render(request,"Extraction/index2.html", {'some_flag': True,'message':"Please enter a username"})
        return HttpResponseRedirect('dashbord/{0}'.format(username))


class DashBordView(View):
    def get(self,request):

        return render(request,template_name="Extraction/dashbored.html")


class PersonalUserDashBordView(View):
    def get(self, request, username):
        myuser = Persons.objects.filter(uname=username)[0]
        # likes,dates=analys_person(username)
        tweets = analys_person(username)
        tweets_df = pd.DataFrame([t.__dict__ for t in tweets])
        print(tweets_df)

        tweets_df["date"] = pd.to_datetime(tweets_df.date, format="%d-%m-%Y %H:%M")
        # convert tweetdf to timeseries df
        for row in (tweets_df,):
            row['Year'] = row.date.dt.year
            row['Month'] = row.date.dt.month
            row['Day'] = row.date.dt.day
            row['Hour'] = row.date.dt.hour

        tweets_df['day of week'] = tweets_df['date'].dt.weekday

        def applyer(row):
            if row.dayofweek == 4 or row.dayofweek == 5:
                return 1
            else:
                return 0

        temp = tweets_df['date'].apply(applyer)
        tweets_df['weekend'] = temp

        tweets_df['Month'] = tweets_df['Month'].apply(lambda x: calendar.month_abbr[x])

        # ---------------------------------------------- personal
        x_data = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        y_data = tweets_df.groupby('day of week').size()
        plot_div1 = plotly_scatter(x_data,
                                   y_data,
                                   color='green',
                                   title='Activity based on days of week',
                                   xlabel='days of week', height=300)

        x_label = list(set(tweets_df['Year']))
        y_data = tweets_df.groupby('Year').size()
        plot_div2 = plotly_pie(x_label,
                               y_data,
                               title="Activity based on year",
                               width=300, height=300
                               )

        plot_div3 = plotly_heatmap(tweets_df)

        return render(request, "Extraction/dash_ploty2.html", context={'plot_div1': plot_div1,
                                                                       'plot_div2': plot_div2,
                                                                       'plot_div3': plot_div3,
                                                                       'uname': username,
                                                                       'myuser':myuser,'followers':human_format(myuser.followers),'followings':human_format(myuser.followings),
                                                                       'datefrom': sorted(list(set(tweets_df['Year'])))[
                                                                           0],
                                                                       'dateto': sorted(list(set(tweets_df['Year'])))[
                                                                           -1]})

class InfluenceUserDashBordView(View):
    def get(self, request, username):
        myuser = Persons.objects.filter(uname=username)[0]
        tweets = analys_person(username)
        tweets_df = pd.DataFrame([t.__dict__ for t in tweets])
        print(tweets_df)

        tweets_df["date"] = pd.to_datetime(tweets_df.date, format="%d-%m-%Y %H:%M")
        # convert tweetdf to timeseries df
        for row in (tweets_df,):
            row['Year'] = row.date.dt.year
            row['Month'] = row.date.dt.month
            row['Day'] = row.date.dt.day
            row['Hour'] = row.date.dt.hour

        tweets_df['day of week'] = tweets_df['date'].dt.weekday

        def applyer(row):
            if row.dayofweek == 4 or row.dayofweek == 5:
                return 1
            else:
                return 0

        temp = tweets_df['date'].apply(applyer)
        tweets_df['weekend'] = temp

        tweets_df['Month'] = tweets_df['Month'].apply(lambda x: calendar.month_abbr[x])

        # ---------------------------------------------- influence---------------------

        x_data = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        y_data=tweets_df.groupby('day of week')['replies_count'].mean()


        plot_div1 = plotly_scatter(x_data,
                                   y_data,
                                   color='green',
                                   title='Average of replies based on week days',
                                   xlabel='days of week', height=300)

        per_month_likes = tweets_df.set_index('date').groupby(pd.Grouper(freq='M'))['likes_count'].mean()

        x = per_month_likes.index
        y = per_month_likes.values
        plot_div2 = plotly_scatter(x,
                                   y,
                                   color='green',
                                   title='Average Of Likes based on Monthes',
                                   xlabel='month in year', height=300)

        per_month_likes = tweets_df.set_index('date').groupby(pd.Grouper(freq='M'))['likes_count'].mean()
        per_month_count = tweets_df.set_index('date').groupby(pd.Grouper(freq='M')).count()['text']
        per_month_influence = per_month_likes.divide(per_month_count)
        x = per_month_influence.index
        y = per_month_influence.values
        plot_div3 = plotly_scatter(x,
                                   y,
                                   color='green',
                                   title='Average Of user popularity(Likes/tweet count) based on Monthes',
                                   xlabel='month in year', height=300)

        per_month_retweet = tweets_df.set_index('date').groupby(pd.Grouper(freq='M'))['retweets_count'].mean()
        per_month_count = tweets_df.set_index('date').groupby(pd.Grouper(freq='M')).count()['text']
        per_month_influence = per_month_retweet.divide(per_month_count)
        x = per_month_influence.index
        y = per_month_influence.values
        plot_div4 = plotly_scatter(x,
                                   y,
                                   color='green',
                                   title='Average Of user popularity(Retweets/tweet count) based on Monthes',
                                   xlabel='month in year', height=300)


        per_month_reply = tweets_df.set_index('date').groupby(pd.Grouper(freq='M'))['replies_count'].mean()
        per_month_count = tweets_df.set_index('date').groupby(pd.Grouper(freq='M')).count()['text']
        per_month_influence = per_month_reply.divide(per_month_count)
        x = per_month_influence.index
        y = per_month_influence.values
        plot_div5 = plotly_scatter(x,
                                   y,
                                   color='green',
                                   title='Average Of user participation(Replies/tweet count) based on Monthes',
                                   xlabel='month in year', height=300)

        return render(request, "Extraction/dash_ploty_influ.html", context={'plot_div1': plot_div1,
                                                                       'plot_div2': plot_div2,
                                                                       'plot_div3': plot_div3,
                                                                       'plot_div4': plot_div4,
                                                                       'plot_div5': plot_div5,
                                                                       'uname': username,
                                                                            'myuser': myuser,
                                                                            'followers': human_format(myuser.followers),
                                                                            'followings': human_format(
                                                                                myuser.followings),
                                                                            'datefrom': sorted(list(set(tweets_df['Year'])))[
                                                                           0],
                                                                       'dateto': sorted(list(set(tweets_df['Year'])))[
                                                                           -1]})