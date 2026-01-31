CREATE TABLE features (
    feature_id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE people (
    person_id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE states (
    state_id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE pbis (
    pbi_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    feature_id TEXT NOT NULL,
    assigned_to TEXT NOT NULL,
    state_id TEXT NOT NULL,
    FOREIGN KEY (feature_id) REFERENCES features(feature_id),
    FOREIGN KEY (assigned_to) REFERENCES people(person_id),
    FOREIGN KEY (state_id) REFERENCES states(state_id)
);

CREATE TABLE comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pbi_id TEXT NOT NULL,
    comment TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (pbi_id) REFERENCES pbis(pbi_id)
);
