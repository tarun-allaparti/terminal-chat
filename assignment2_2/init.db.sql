CREATE TABLE IF NOT EXISTS commands (
    id SERIAL PRIMARY KEY,
    command VARCHAR(20),
    server_url VARCHAR(200)
);