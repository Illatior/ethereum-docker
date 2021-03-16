CREATE USER dockeruser;
GRANT ALL PRIVILEGES ON DATABASE postgres TO dockeruser;

CREATE TABLE blocks (
    id SERIAL PRIMARY KEY,
    block_id INTEGER UNIQUE NOT NULL,
    block_time BIGINT NOT NULL
);