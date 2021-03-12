import mysql.connector
from config import Settings
import pandas as pd
import time
import datetime
from config import Dbsettings



def storage(table, tracked_word, id_tweet, created_at, text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count,longitude, latitude,\
                retweet_count, favorite_count):

    mydb = mysql.connector.connect(
    host=Dbsettings.HOST2,
    user=Dbsettings.USER2,
    passwd=Dbsettings.PASSWORD2,
    database=Dbsettings.DATABASE2,
    port=Dbsettings.PORT2,
    charset = 'utf8'
    )
    
    print('Entramos')
    print(mydb.is_connected())
    if mydb.is_connected():
        mycursor = mydb.cursor()
        mycursor.execute(f'CREATE TABLE IF NOT EXISTS {table} ({Settings.TABLE_ATTRIBUTES_2})')
        #Insert if not exist the word column has a UNIQUE CONSTRAINT
        try:
            mycursor.execute(f"INSERT INTO newtrackwords (word) VALUES ('{tracked_word}')")
            mydb.commit()
        except mysql.connector.IntegrityError as err:
            print('Word already in the Database.')

        #Query the id of the tracked word
        query_word_id = f"SELECT word_id FROM newtrackwords WHERE word='{tracked_word}'"
        
        mycursor.execute(query_word_id)
        word_ids = mycursor.fetchall()
        word_id = word_ids[0][0]
       
        val = (word_id, id_tweet, created_at, text, polarity, subjectivity, user_created_at, \
             user_location, user_description, user_followers_count, longitude, latitude,\
                  retweet_count, favorite_count)
        print(val)
        sql = "INSERT INTO {} (word_id, id_tweet, created_at, text, polarity, subjectivity, \
            user_created_at, user_location, user_description, user_followers_count, \
            longitude, latitude, retweet_count, favorite_count)\
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table)

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



