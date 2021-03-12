import os

class Credentials:
    API_KEY = os.getenv('API_KEY')
    API_SECRET_KEY = os.getenv('API_SECRET_KEY')
    #tokens
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_SECRET_TOKEN')

class Settings:
    TRACK_WORDS = 'Technology'
    TABLE_NAME = "twttechnology"
    TABLE_ATTRIBUTES = "id INTEGER PRIMARY KEY AUTO_INCREMENT, id_tweet VARCHAR(255), created_at DATETIME, text VARCHAR(255), \
            polarity INT, subjectivity INT, user_created_at VARCHAR(255), \
            user_location VARCHAR(255), user_description VARCHAR(255), \
            user_followers_count INT, longitude DOUBLE, latitude DOUBLE, \
            retweet_count INT, favorite_count INT"
    
    TABLE_ATTRIBUTES_2 = "id INTEGER PRIMARY KEY AUTO_INCREMENT, \
        word_id INTEGER, id_tweet VARCHAR(255), created_at DATETIME, text VARCHAR(255), \
        polarity INT, subjectivity INT, user_created_at VARCHAR(255), \
        user_location VARCHAR(255), user_description VARCHAR(255), \
        user_followers_count INT, longitude DOUBLE, latitude DOUBLE, \
        retweet_count INT, favorite_count INT"

class Dbsettings:
    HOST = os.getenv('MYSQL_HOST')
    USER = os.getenv('MYSQL_USER')
    PASSWORD = os.getenv('MYSQL_PASSWORD')
    DATABASE = os.getenv('MYSQL_DB')
    PORT = os.getenv('MYSQL_PORT')
    
    #DATA BASE FOR NLP TECH PROJECT
    HOST2 = os.getenv('MYSQL_HOST_2')
    USER2 = os.getenv('MYSQL_USER_2')
    PASSWORD2 = os.getenv('MYSQL_PASSWORD_2')
    DATABASE2 = os.getenv('MYSQL_DB_2')
    PORT2 = os.getenv('MYSQL_PORT_2')

