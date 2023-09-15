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

INSERT INTO veld_repo (local_path) VALUES ('path_a');
INSERT INTO veld (commit, veld_repo_id) VALUES ('commit_a', 1);
INSERT INTO veld (commit, veld_repo_id) VALUES ('commit_b', 1);