import pandas as pd  # type: ignore
from config import IMDB_PATH

def recommend_by_genre(liked_movies, top_n=5):

    # Load movie dataset
    df_imbd = pd.read_csv(IMDB_PATH)

    # ---------------- COLD START HANDLE ----------------
    # if no liked movies → return top rated movies
    if not liked_movies:
        print("No liked movies → returning default top rated movies")
        return df_imbd.sort_values(
            "IMDB_Rating", ascending=False
        )["Series_Title"].head(top_n).tolist()
    # ---------------------------------------------------

    # Task 1: extract genres from liked movies
    liked_genre_temp = []

    for title in liked_movies:
        row = df_imbd[df_imbd["Series_Title"] == title]

        if row.empty:
            continue

        genre = row.iloc[0]["Genre"].split(",")

        for g in genre:
            liked_genre_temp.append(g.strip())

    # safety check — if no genres extracted (edge case)
    if not liked_genre_temp:
        print("Liked movies had no genre match → fallback to top rated")
        return df_imbd.sort_values(
            "IMDB_Rating", ascending=False
        )["Series_Title"].head(top_n).tolist()

    # Task 2: calculate genre frequency score
    genre_score = {}

    for g in liked_genre_temp:
        genre_score[g] = genre_score.get(g, 0) + 1

    recommendations = []

    # Task 3: score all other movies
    for index, row in df_imbd.iterrows():
        title = row["Series_Title"]
        IMDB_rating = row["IMDB_Rating"]

        if title in liked_movies:
            continue

        movie_genres = [g.strip() for g in row["Genre"].split(",")]

        score = 0
        for g in movie_genres:
            score += genre_score.get(g, 0)

        if score > 0:
            recommendations.append((title, score, IMDB_rating))

    # sort by (genre score, imdb rating)
    recommendations.sort(key=lambda i: (i[1], i[2]), reverse=True)

    # return top N movie names
    recommendations_movies_name = [
        title for title, score, rating in recommendations[:top_n]
    ]

    return recommendations_movies_name
