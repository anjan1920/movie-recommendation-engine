import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def get_similar_users(user_id, min_similarity=0.1, top_n=10):

    # load the matrix
    df = pd.read_csv('user_item_matrix.csv')

    # ensure user_id type consistency
    df["user_id"] = df["user_id"].astype(type(user_id))

    if user_id not in df['user_id'].values:
        return []

    user_ids = df['user_id'].values
    movie_matrix = df.drop(columns=['user_id']).values

    user_idx = np.where(user_ids == user_id)[0][0]
    target_vector = movie_matrix[user_idx]

    # If user has no liked movies → similarity meaningless
    if np.sum(target_vector) == 0:
        return []

    similarity_scores = cosine_similarity(target_vector.reshape(1, -1), movie_matrix)[0]

    similar_users = []

    for i in range(len(similarity_scores)):
        if i == user_idx:
            continue
        if similarity_scores[i] < min_similarity:
            continue

        similar_users.append((user_ids[i], similarity_scores[i]))

    similar_users.sort(key=lambda x: x[1], reverse=True)

    return similar_users[:top_n]
