CREATE TABLE Users (
    id          INTEGER PRIMARY KEY,
    email       TEXT NOT NULL,
    name        TEXT NOT NULL
);

CREATE TABLE Accounts(
    id          INTEGER PRIMARY KEY,
    userName    TEXT NOT NULL,
    user_id     INTEGER NOT NULL
);

CREATE TABLE Posts (
    id          INTEGER PRIMARY KEY,
    title       TEXT NOT NULL,
    textBody    TEXT NOT NULL,
    date        dateTime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    posterId    INTEGER NOT NULL,
    FOREIGN KEY (posterId) REFERENCES Users(id)
);

CREATE TABLE Comments (
    id          INTEGER PRIMARY KEY,
    textBody    TEXT NOT NULL,
    commenterId INTEGER NOT NULL,
    postId      INTEGER NOT NULL,
    FOREIGN KEY (commenterId) REFERENCES Users(id),
    FOREIGN KEY (postId) REFERENCES Posts(id)
);

CREATE TABLE Likes (
    id          INTEGER PRIMARY KEY,
    userId      INTEGER NOT NULL,
    postId      INTEGER NOT NULL,
    FOREIGN KEY (userId) REFERENCES Users(id),
    FOREIGN KEY (postId) REFERENCES Posts(id)
);

CREATE TABLE Follows (
    id          INTEGER PRIMARY KEY,
    followerId  INTEGER NOT NULL,
    followeeId  INTEGER NOT NULL,
    FOREIGN KEY (followerId) REFERENCES Users(id),
    FOREIGN KEY (followeeId) REFERENCES Users(id)
);
