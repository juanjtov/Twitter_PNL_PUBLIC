import pandas as pd
import plotly
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import itertools
import math
import time
import datetime

from config import Settings
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Filter constants for states in COL
COUNTRIES = ['Argentina', 'ARG', 'Bolivia', 'BOL', 'Brazil', 'BRA', 'Chile', 'CHL', 'Colombia', 'COL', 'Ecuador', 'ECU', 'Falkland', 'Islands', 'FLK', 'French', 'Guiana', 'GUF', 'Guiana', 'GUF', 'Guyana', 'GUY', 'Paraguay', 'PRY', 'Peru', 'PER', 'Suriname', 'SUR', 'Uruguay', 'URY', 'Venezuela', 'VEN']
COUNTRY_DICT = dict(itertools.zip_longest(*[iter(COUNTRIES)] * 2, fillvalue=""))
INV_COUNTRY_DICT = dict((v,k) for k,v in COUNTRY_DICT.items())

def clean_transform_data(df):
    #As we only display real-time tweets posted in last 30 minutes, groups of 2-second interval could best display on the screen in practice
    result = df.groupby([pd.Grouper(key='created_at', freq='2s'), 'polarity']).count().unstack(fill_value=0).stack().reset_index()
    result = result.rename(columns={"id_tweet": "Num of {} mentions".format(Settings.TRACK_WORDS), "created_at":"Time in UTC"})  
    #Record the time series with 2-second interval for further index usage.
    time_series = result["Time in UTC"][result['polarity']==0].reset_index(drop=True)
    return result, time_series

def plot_results(result, time_series, fd, geo_dist):
    #The data frame must have information
    
    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[1, 0.4],
        row_heights=[0.6, 0.4],
        specs=[[{"type": "scatter", "rowspan": 2}, {"type": "choropleth"}],
               [            None                    , {"type": "bar"}]],
        subplot_titles= ("Sentiment analysis", "Words Frequency", "", "Countries In Action")
        )
    fig.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of {} mentions".format(Settings.TRACK_WORDS)][result['polarity']==0].reset_index(drop=True),
        name="Neutral",
        opacity=0.8), row=1, col=1)   
    fig.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of {} mentions".format(Settings.TRACK_WORDS)][result['polarity']==-1].reset_index(drop=True),
        name="Negative",
        opacity=0.8), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of {} mentions".format(Settings.TRACK_WORDS)][result['polarity']==1].reset_index(drop=True),
        name="Positive",
        opacity=0.8), row=1, col=1)

    # Plot Bar chart   
    fig.add_trace(go.Bar(x=fd["Word"], y=fd["Frequency"], name="Freq Dist"), row=2, col=2)
    # 59, 89, 152
    fig.update_traces(marker_color='rgb(59, 89, 152)', marker_line_color='rgb(8,48,107)', \
            marker_line_width=0.5, opacity=0.7, row=2, col=2)

    #chloropleth graph
    fig.add_trace(go.Choropleth(
        locations=geo_dist['Country'], # Spatial coordinates
        z = geo_dist['Log Num'].astype(float), # Data to be color-coded
        #locationmode = 'USA-states', it takes ISO BY DEFAULT # set of locations match entries in `locations`
        colorscale = "Blues",
        text=geo_dist['text'], # hover text
        showscale=True,
        geo = 'geo'
        ),
        row=1, col=2)
    
    fig.update_layout(
        title_text= "Real-time tracking '{}' mentions on Twitter {} UTC".format(Settings.TRACK_WORDS ,datetime.datetime.utcnow().strftime('%m-%d %H:%M')),
        geo = dict(
            scope='south america',
        ),
        template="plotly_dark",
        margin=dict(r=20, t=50, b=50, l=90),
        annotations=[
            go.layout.Annotation(
                text="Source: Twitter",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=0)
        ],
        showlegend=True,
        xaxis_rangeslider_visible=True)


    
         

#        subplot_titles= ("Sentiment analysis", "Words Frequency", "", "Countries In Action")
    fig.show()


def pnl_module(df):
    content = ' '.join(df["text"])
    content = re.sub(r"http\S+", "", content)
    content = content.replace('RT ', ' ').replace('&amp;', 'and')
    content = re.sub('[^A-Za-z0-9]+', ' ', content)
    content = content.lower()
   

    tokenized_word = word_tokenize(content)
    #Extra  fine filter
    tokenized_word = [word for word in tokenized_word if len(word)>3]
    stop_words=set(stopwords.words("spanish"))
    filtered_sent=[]
    for w in tokenized_word:
        if w not in stop_words:
            filtered_sent.append(w)
    fdist = FreqDist(filtered_sent)
    fd = pd.DataFrame(fdist.most_common(15), columns = ["Word","Frequency"]).drop([0]).reindex()

    return fd

def geo_distr_data(df):
    is_in_SA=[]
    #geo = df[['user_location']]
    df = df.fillna(" ")
    for x in df['user_location']:
        check = False
        for c in COUNTRIES:
            if c in x:
                is_in_SA.append(COUNTRY_DICT[c] if c in COUNTRY_DICT else c)
                check = True
                break
        if not check:
            is_in_SA.append(None)

    geo_dist = pd.DataFrame(is_in_SA, columns=['Country']).dropna().reset_index()
    geo_dist = geo_dist.groupby('Country').count().rename(columns={"index": "Number"}) \
            .sort_values(by=['Number'], ascending=False).reset_index()
    geo_dist["Log Num"] = geo_dist["Number"].apply(lambda x: math.log(x, 2))


    geo_dist['Full Country Name'] = geo_dist['Country'].apply(lambda x: INV_COUNTRY_DICT[x])
    geo_dist['text'] = geo_dist['Full Country Name'] + '<br>' + 'Num: ' + geo_dist['Number'].astype(str)

    return geo_dist



