SELECT CURRENT_DATE;

-- Drop all tables
DROP TABLE IF EXISTS bookmarks;

--users

CREATE TABLE bookmarks (
    id serial PRIMARY KEY,
    title text NOT NULL,
    url text NOT NULL,
    rating int,
    description text
);

INSERT INTO bookmarks (title, url, rating, description) VALUES
    (
        'Google',
        'https://www.google.com',
        5,
        'Best search engine on the web'
    ),
    (
        'Github',
        'https://github.com',
        5,
        'Most popular repository hosting service on the web'
    );

