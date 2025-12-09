# config.py

CACHE_FILE = "islamabad_full_v9.pkl"
DB_FILE = "points.db"

TRAFFIC_SCHEDULE = [
    (7, 9, 0.4),
    (9, 12, 0.8),
    (12, 14, 0.9),
    (14, 16, 0.7),
    (16, 19, 0.3),
    (19, 21, 0.6),
    (21, 24, 1.0),
    (0, 7, 1.0),
]

MODE_CONFIG = {
    "car": {
        "speeds": {
            "motorway": 100,
            "trunk": 80,
            "primary": 60,
            "secondary": 45,
            "tertiary": 35,
            "residential": 30,
        },
        "forbidden": [],
        "traffic_impact": 1.0,
    },
    "bike": {
        "speeds": {
            "motorway": 0,
            "trunk": 60,
            "primary": 50,
            "secondary": 40,
            "tertiary": 35,
            "residential": 30,
        },
        "forbidden": ["motorway", "motorway_link"],
        "traffic_impact": 0.3,
    },
}