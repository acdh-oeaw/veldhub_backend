CREATE TABLE veld_repo (
    id SERIAL PRIMARY KEY,
    local_path TEXT,
    remote_url TEXT,
    head_commit TEXT
);

CREATE TABLE veld (
    id SERIAL PRIMARY KEY,
    commit TEXT UNIQUE,
    file_name TEXT,
    veld_repo_id INTEGER NOT NULL,
    CONSTRAINT fk_veld_repo_id FOREIGN KEY (veld_repo_id) REFERENCES veld_repo (id)
);
