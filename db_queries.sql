CREATE TABLE IF NOT EXISTS `twtanalysis` (id INTEGER PRIMARY KEY AUTO_INCREMENT, \
            id_tweet VARCHAR(255), word_id INTEGER, FOREIGN KEY (word_id) REFERENCES trackwords(word_id), \
            created_at DATETIME, text VARCHAR(255), \
            polarity INTEGER, subjectivity INT, user_created_at VARCHAR(255), \
            user_location VARCHAR(255), user_description VARCHAR(255), \
            user_followers_count INTEGER, longitude DOUBLE, latitude DOUBLE, \
            retweet_count INTEGER, favorite_count INTEGER) ;

