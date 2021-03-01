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

def storage(id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count,longitude, latitude,\
                retweet_count, favorite_count):
    if mydb.is_connected():
        mycursor = mydb.cursor()
        val = (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, \
              user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count)
        sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count, \
               longitude, latitude, retweet_count, favorite_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(Settings.TABLE_NAME)
        
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
    timenow = (datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=20)).strftime('%Y-%m-%d %H:%M:%S')

    #make the query
    query = f"SELECT id_str, text, created_at, polarity, user_location FROM {Settings.TABLE_NAME} WHERE created_at >= '{timenow}' "
    df = pd.read_sql(query, con=db_connection)
    
    #CONVERT DATATIME(MySQL data type) into Datetime (Pandas)
    # UTC for date time at default
    df['created_at'] = pd.to_datetime(df['created_at'])
   
    return df



