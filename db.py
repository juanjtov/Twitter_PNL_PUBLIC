import mysql.connector
from config import Settings
import pandas as pd
import time
import datetime
from config import Dbsettings



mydb = mysql.connector.connect(
    host=Dbsettings.HOST,
    user=Dbsettings.USER,
    passwd=Dbsettings.PASSWORD,
    database=Dbsettings.DATABASE,
    port=Dbsettings.PORT,
    charset = 'utf8'
)

if mydb.is_connected():
    mycursor = mydb.cursor()
    mycursor.execute(f'CREATE TABLE IF NOT EXISTS {Settings.TABLE_NAME} ({Settings.TABLE_ATTRIBUTES})')
    mydb.commit()

    mycursor.close()

def storage(tracked_word, id_tweet, created_at, text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count,longitude, latitude,\
                retweet_count, favorite_count):
    
    print('Entramos')
    if mydb.is_connected():
        mycursor = mydb.cursor()
        #Tracked words query
        query_word_id = f"SELECT word_id FROM trackwords WHERE word='{tracked_word}'"
        
        mycursor.execute(query_word_id)
        word_ids = mycursor.fetchall()
        print(word_ids)
        word_id = word_ids[0][0]
        print(word_id)
        val = (id_tweet, word_id, created_at, text, polarity, subjectivity, user_created_at, \
             user_location, user_description, user_followers_count, longitude, latitude,\
                  retweet_count, favorite_count)
        print(val)
        sql = "INSERT INTO twtanalysis (id_tweet, word_id, created_at, text, polarity, subjectivity, \
            user_created_at, user_location, user_description, user_followers_count, \
            longitude, latitude, retweet_count, favorite_count)\
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        print(sql)
        
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()

def extracting_tweets():
    
    db_connection = mysql.connector.connect(
    host = Dbsettings.HOST,
    user = Dbsettings.USER,
    passwd = Dbsettings.PASSWORD,
    database = Dbsettings.DATABASE,
    port = Dbsettings.PORT, 
    charset = 'utf8'
    )

    #Load data from MySQL
    #how many data
    timenow = (datetime.datetime.utcnow() - datetime.timedelta(hours=3, minutes=20)).strftime('%Y-%m-%d %H:%M:%S')

    #make the query
    query = f"SELECT id_tweet, word_id, text, created_at, polarity, user_location \
             FROM twtanalysis WHERE created_at >= '{timenow}' "
    df = pd.read_sql(query, con=db_connection)
    
    #CONVERT DATATIME(MySQL data type) into Datetime (Pandas)
    # UTC for date time at default
    df['created_at'] = pd.to_datetime(df['created_at'])
   
    return df



