from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


@dataclass
class Song:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    songs = []
    float_columns = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for col in float_columns:
                if col in row:
                    row[col] = float(row[col])
            songs.append(row)
    return songs


def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
    WEIGHTS = {
        "genre":        0.15,
        "mood":         0.25,
        "energy":       0.30,
        "tempo_bpm":    0.10,
        "valence":      0.10,
        "danceability": 0.05,
        "acousticness": 0.05,
    }

    reasons = []

    def numeric_score(song_val: float, pref_val: float, value_range: float) -> float:
        return max(0.0, 1.0 - abs(song_val - pref_val) / value_range)

    genre_score = 1.0 if song.get("genre") == user_prefs.get("genre") else 0.0
    mood_score  = 1.0 if song.get("mood")  == user_prefs.get("mood")  else 0.0

    genre_contrib = WEIGHTS["genre"] * genre_score
    mood_contrib  = WEIGHTS["mood"]  * mood_score

    if genre_score == 1.0:
        reasons.append(f"genre match (+{genre_contrib:.2f})")
    if mood_score == 1.0:
        reasons.append(f"mood match (+{mood_contrib:.2f})")

    numeric_attrs = [
        ("energy",       user_prefs.get("energy",       0.5),  1.0),
        ("tempo_bpm",    user_prefs.get("tempo_bpm",    120),   140.0),
        ("valence",      user_prefs.get("valence",      0.5),  1.0),
        ("danceability", user_prefs.get("danceability", 0.5),  1.0),
        ("acousticness", user_prefs.get("acousticness", 0.5),  1.0),
    ]

    total = genre_contrib + mood_contrib
    for attr, pref_val, value_range in numeric_attrs:
        attr_score = numeric_score(float(song[attr]), pref_val, value_range)
        contrib    = WEIGHTS[attr] * attr_score
        total     += contrib
        reasons.append(f"{attr} similarity (+{contrib:.2f})")

    if not reasons:
        reasons.append("general profile similarity")

    return round(max(0.0, min(1.0, total)), 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    def to_result(song: Dict):
        score, reasons = score_song(song, user_prefs)
        return (song, score, ", ".join(reasons))

    return sorted(
        [to_result(song) for song in songs],
        key=lambda x: (-x[1], x[0].get("id", 0)),
    )[:k]


class Recommender:
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood":  user.favorite_mood,
            "energy": user.target_energy,
            "acousticness": 1.0 if user.likes_acoustic else 0.0,
        }
        song_dicts = [s.__dict__ for s in self.songs]
        ranked = recommend_songs(user_prefs, song_dicts, k=k)
        top_ids = {r[0]["id"] for r in ranked}
        return [s for s in self.songs if s.id in top_ids][:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood":  user.favorite_mood,
            "energy": user.target_energy,
            "acousticness": 1.0 if user.likes_acoustic else 0.0,
        }
        _, reasons = score_song(song.__dict__, user_prefs)
        return ", ".join(reasons)