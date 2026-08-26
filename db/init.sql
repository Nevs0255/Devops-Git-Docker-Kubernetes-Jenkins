CREATE TABLE IF NOT EXISTS releves (
    ville       TEXT PRIMARY KEY,
    temperature INTEGER NOT NULL
);

INSERT INTO releves (ville, temperature) VALUES
    ('Paris', 21),
    ('Lyon', 24),
    ('Marseille', 27),
    ('Lille', 18),
    ('Bordeaux', 25)
ON CONFLICT (ville) DO NOTHING;
