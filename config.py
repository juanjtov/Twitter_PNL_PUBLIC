import os

class Credentials:
    API_KEY = 'TWT_API_KEY'
    API_SECRET_KEY = 'TWT_API_SECRET_KEY'
    #tokens
    ACCESS_TOKEN = 'TWT_ACCESS_TOKEN'
    ACCESS_TOKEN_SECRET = 'TWT_SECRET_ACCESS_TOKEN'

class Settings:
    TRACK_WORDS = 'Colombia'
    TABLE_NAME = "Colombia"
    TABLE_ATTRIBUTES = "id_str VARCHAR(255), created_at DATETIME, text VARCHAR(255), \
            polarity INT, subjectivity INT, user_created_at VARCHAR(255), user_location VARCHAR(255), \
            user_description VARCHAR(255), user_followers_count INT, longitude DOUBLE, latitude DOUBLE, \
            retweet_count INT, favorite_count INT"

class Dbsettings:
    HOST = os.getenv('MYSQL_HOST')
    USER = os.getenv('MYSQL_USER')
    PASSWORD = os.getenv('MYSQL_PASSWORD')
    DATABASE = os.getenv('MYSQL_DB')
    PORT = os.getenv('MYSQL_PORT')

