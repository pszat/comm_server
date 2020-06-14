CREATE TABLE users(
    id SERIAL NOT NULL PRIMARY KEY,
    username VARCHAR(60),
    email VARCHAR(60) UNIQUE,
    hashed_password VARCHAR(1024)
    );