"""
Command line runner for the Music Recommender Simulation.
"""
import subprocess
import sys
from pathlib import Path
from src.recommender import load_songs, recommend_songs


def _reliability_check() -> bool:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "tests/test_reliability.py"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("Reliability tests failed. Not generating recommendations.\n")
            print(result.stdout)
            print(result.stderr)
            return False
        print("All reliability tests passed.\n")
        return True
    except FileNotFoundError:
        print("Error: pytest not found. Install it with: pip install pytest")
        return False
    except Exception as e:
        print(f"Unexpected error during reliability check: {e}")
        return False


def main() -> None:
    if not _reliability_check():
        return

    csv_path = "data/songs.csv"
    if not Path(csv_path).exists():
        print(f"Error: CSV file not found at '{csv_path}'")
        return

    try:
        songs = load_songs(csv_path)
    except Exception as e:
        print(f"Error loading songs: {e}")
        return

    if not songs:
        print("No songs found in the dataset.")
        return

    genres = sorted({s.get("genre", "").strip().lower() for s in songs if s.get("genre")})
    moods = sorted({s.get("mood", "").strip().lower() for s in songs if s.get("mood")})

    print(f"Available genres: {', '.join(genres)}")
    genre = input("Enter a genre: ").strip().lower()

    print(f"Available moods: {', '.join(moods)}")
    mood = input("Enter a mood: ").strip().lower()

    user_prefs4 = {"genre": genre, "mood": mood}

    try:
        recommendations = recommend_songs(user_prefs4, songs, k=5)
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return

    if not recommendations:
        print("No recommendations found for the given preferences.")
        return

    print("\nTop recommendations:\n")
    for rec in recommendations:
        try:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()
        except (KeyError, ValueError) as e:
            print(f"Error displaying recommendation: {e}")
            continue


if __name__ == "__main__":
    main()