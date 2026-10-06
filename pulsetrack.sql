-- PulseTrack database (SQLite)
-- Rebuilt from the week 2 lab slides. Run with: python create_db.py
-- Starts with DROP TABLE IF EXISTS, so running it again gives a fresh database.

DROP TABLE IF EXISTS activities;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    email        TEXT    NOT NULL UNIQUE,
    display_name TEXT    NOT NULL,
    role         TEXT    NOT NULL DEFAULT 'athlete' CHECK (role IN ('athlete', 'coach', 'admin')),
    created_at   TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE activities (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    sport       TEXT    NOT NULL CHECK (sport IN ('run', 'ride', 'swim', 'gym')),
    title       TEXT    NOT NULL,
    started_at  TEXT    NOT NULL,
    duration_s  INTEGER NOT NULL CHECK (duration_s > 0),
    distance_m  REAL    NOT NULL DEFAULT 0 CHECK (distance_m >= 0),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- 5 users
INSERT INTO users (email, display_name, role, created_at) VALUES
    ('emma@example.com',  'Emma Peeters',  'admin',   '2026-09-01T09:00:00+02:00'),
    ('lucas@example.com', 'Lucas Janssens', 'athlete', '2026-09-02T10:15:00+02:00'),
    ('noor@example.com',  'Noor El Amrani', 'athlete', '2026-09-03T08:30:00+02:00'),
    ('milan@example.com', 'Milan Wouters', 'coach',   '2026-09-04T14:00:00+02:00'),
    ('lotte@example.com', 'Lotte Maes',    'athlete', '2026-09-05T11:45:00+02:00');

-- 16 activities (Noor = user 3 has four of them)
INSERT INTO activities (user_id, sport, title, started_at, duration_s, distance_m) VALUES
    (1, 'run',  'Morning run along the canal', '2026-09-14T07:30:00+02:00', 2700,  7200),
    (2, 'ride', 'Evening ride',                '2026-09-14T18:00:00+02:00', 5400, 32000),
    (3, 'swim', 'Pool laps',                   '2026-09-15T06:45:00+02:00', 2400,  1800),
    (4, 'gym',  'Leg day',                     '2026-09-15T19:00:00+02:00', 3600,     0),
    (5, 'run',  'Easy recovery run',           '2026-09-16T07:00:00+02:00', 1800,  4500),
    (1, 'ride', 'Ride to the coast',           '2026-09-17T17:30:00+02:00', 7200, 45000),
    (3, 'run',  'Interval session',            '2026-09-18T07:15:00+02:00', 2400,  6000),
    (2, 'swim', 'Lunch swim',                  '2026-09-19T12:00:00+02:00', 1800,  1500),
    (5, 'gym',  'Core and mobility',           '2026-09-20T10:00:00+02:00', 2700,     0),
    (3, 'ride', 'Sunday group ride',           '2026-09-21T09:00:00+02:00', 10800, 68000),
    (4, 'run',  'Tempo run',                   '2026-09-22T07:00:00+02:00', 2100,  6500),
    (1, 'swim', 'Open water swim',             '2026-09-23T06:30:00+02:00', 2700,  2500),
    (3, 'run',  'Long run',                    '2026-09-26T07:00:00+02:00', 5400, 15000),
    (2, 'run',  'Hill repeats',                '2026-09-24T18:30:00+02:00', 3000,  7000),
    (5, 'ride', 'Commute ride',                '2026-09-25T17:00:00+02:00', 1500,  8000),
    (4, 'gym',  'Upper body',                  '2026-09-27T18:00:00+02:00', 3600,     0);
