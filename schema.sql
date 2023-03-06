DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS exercisetypes;
DROP TABLE IF EXISTS exercises;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE exercisetypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    exercisetype_id INTEGER NOT NULL,
    duration_minutes INTEGER NOT NULL,
    date_completed DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exercisetype_id) REFERENCES exercisetypes(id)
);