import random
from pathlib import Path

from src.recommender import load_songs, score_song, recommend_songs


def _sample_songs():
    return [
        {
            "id": 1,
            "title": "Pop Spark",
            "artist": "A",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "tempo_bpm": 128.0,
            "valence": 0.80,
            "danceability": 0.82,
            "acousticness": 0.10,
        },
        {
            "id": 2,
            "title": "Lofi Cloud",
            "artist": "B",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "tempo_bpm": 92.0,
            "valence": 0.50,
            "danceability": 0.55,
            "acousticness": 0.72,
        },
        {
            "id": 3,
            "title": "Rock Drive",
            "artist": "C",
            "genre": "rock",
            "mood": "energetic",
            "energy": 0.92,
            "tempo_bpm": 138.0,
            "valence": 0.74,
            "danceability": 0.76,
            "acousticness": 0.08,
        },
    ]


def test_load_songs_parses_numeric_types(tmp_path: Path):
    csv_file = tmp_path / "songs.csv"
    csv_file.write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
        "1,Song A,Artist A,pop,happy,0.8,120,0.7,0.75,0.2\n",
        encoding="utf-8",
    )

    songs = load_songs(str(csv_file))
    s = songs[0]

    assert isinstance(s["id"], int)
    assert isinstance(s["energy"], float)
    assert isinstance(s["tempo_bpm"], float)
    assert isinstance(s["valence"], float)
    assert isinstance(s["danceability"], float)
    assert isinstance(s["acousticness"], float)


def test_score_song_stays_in_range_and_has_reasons():
    song = _sample_songs()[0]
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, reasons = score_song(song, prefs)

    assert 0.0 <= score <= 1.0
    assert isinstance(reasons, list)
    assert len(reasons) > 0


def test_perfect_match_scores_higher_than_clear_mismatch():
    song = _sample_songs()[0]
    perfect = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "tempo_bpm": 128.0,
        "valence": 0.80,
        "danceability": 0.82,
        "acousticness": 0.10,
    }
    mismatch = {
        "genre": "metal",
        "mood": "sad",
        "energy": 0.1,
        "tempo_bpm": 60.0,
        "valence": 0.1,
        "danceability": 0.1,
        "acousticness": 0.95,
    }

    score_perfect, _ = score_song(song, perfect)
    score_mismatch, _ = score_song(song, mismatch)

    assert score_perfect > score_mismatch


def test_recommend_songs_respects_k_and_sorted_desc():
    songs = _sample_songs()
    prefs = {"genre": "rock", "mood": "energetic", "energy": 0.9}

    top = recommend_songs(prefs, songs, k=2)
    assert len(top) == 2
    assert top[0][1] >= top[1][1]


def test_recommend_songs_is_deterministic_same_input():
    songs = _sample_songs()
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.4}

    r1 = recommend_songs(prefs, songs, k=3)
    r2 = recommend_songs(prefs, songs, k=3)

    assert r1 == r2


def test_randomized_reliability_no_crash_and_valid_scores():
    random.seed(42)
    songs = _sample_songs()

    for _ in range(100):
        prefs = {
            "genre": random.choice(["pop", "rock", "lofi", "jazz"]),
            "mood": random.choice(["happy", "chill", "energetic", "sad"]),
            "energy": random.random(),
            "tempo_bpm": random.uniform(60, 180),
            "valence": random.random(),
            "danceability": random.random(),
            "acousticness": random.random(),
        }
        recs = recommend_songs(prefs, songs, k=3)
        assert len(recs) == 3
        for _, score, explanation in recs:
            assert 0.0 <= score <= 1.0
            assert isinstance(explanation, str)
            assert len(explanation) > 0