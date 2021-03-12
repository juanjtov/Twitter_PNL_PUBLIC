CREATE TABLE IF NOT EXISTS `fulltweetfile` (id INTEGER PRIMARY KEY AUTO_INCREMENT, \
            id_tweet VARCHAR(255), word_id INTEGER, FOREIGN KEY (word_id) REFERENCES trackwords(word_id), \
            created_at DATETIME, text VARCHAR(255), \
            polarity INTEGER, subjectivity INT, user_created_at VARCHAR(255), \
            user_location VARCHAR(255), user_description VARCHAR(255), \
            user_followers_count INTEGER, longitude DOUBLE, latitude DOUBLE, \
            retweet_count INTEGER, favorite_count INTEGER) ;

CREATE TABLE IF NOT EXISTS `twtechanalysis` (id INTEGER PRIMARY KEY AUTO_INCREMENT, \
            id_tweet VARCHAR(255), word_id INTEGER, FOREIGN KEY (word_id) REFERENCES trackwords(word_id), \
            created_at DATETIME, text VARCHAR(255), \
            polarity INTEGER, subjectivity INT, user_created_at VARCHAR(255), \
            user_location VARCHAR(255), user_description VARCHAR(255), \
            user_followers_count INTEGER, longitude DOUBLE, latitude DOUBLE, \
            retweet_count INTEGER, favorite_count INTEGER) ;

SELECT id_tweet, word_id, text, created_at, polarity, \
user_location  FROM Colombia \
WHERE created_at >=  2021-03-02 02:09:27;

INSERT INTO `trackwords` (word) VALUES ('bucaramanga');


SELECT word, COUNT(word) \
FROM trackwords \
GROUP BY word  \
HAVING COUNT(word) > 1 ;
     
SELECT * FROM `trackwords` AS du \
WHERE (
    SELECT COUNT(*)
    FROM `trackwords` AS innr
    WHERE du.word = innr.word
);

SELECT (trackwords.word)::text, COUNT(*) \
FROM `trackwords` \
GROUP BY trackwords.word \
HAVING COUNT(*) > 1;

CREATE TABLE IF NOT EXISTS newtrackwords (
    word_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    word VARCHAR(100) NOT NULL
);

INSERT INTO `newtrackwords`  (word)
SELECT DISTINCT word 
FROM trackwords;


ALTER TABLE `newtrackwords` ADD UNIQUE (word);