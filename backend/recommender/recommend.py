import pandas as pd
from config import MATRIX_PATH, IMDB_PATH


def recommend_movies(user_id, similar_users, top_n=5):

    user_item = pd.read_csv(MATRIX_PATH)
    movies = pd.read_csv(IMDB_PATH)

    # ensure consistent user_id type
    user_item["user_id"] = user_item["user_id"].astype(type(user_id))

    if user_id not in user_item["user_id"].values:
        return []

    # Movies watched by target user
    user_row = user_item[user_item["user_id"] == user_id]
    user_row = user_row.drop(columns=["user_id"])

    user_watched = set()
    for col in user_row.columns:
        if user_row.iloc[0][col] == 1:
            user_watched.add(col)

    movie_scores = {}

    # Loop through similar users
    for sim_user_id, sim_score in similar_users:
        sim_row = user_item[user_item["user_id"] == sim_user_id]
        if sim_row.empty:
            continue

        sim_row = sim_row.drop(columns=["user_id"])

        for col in sim_row.columns:
            if sim_row.iloc[0][col] == 1 and col not in user_watched:
                movie_scores[col] = movie_scores.get(col, 0) + sim_score

    if not movie_scores:
        return []

    ranked_movies = sorted(movie_scores.items(), key=lambda item: item[1], reverse=True)

    # Convert movie IDs → titles safely
    recommendations = []
    for movie_id, _ in ranked_movies[:top_n]:
        movie_row = movies[movies.index.astype(str) == movie_id]
        if movie_row.empty:
            continue
        title = movie_row.iloc[0]["Series_Title"]
        recommendations.append(title)

    return recommendations
