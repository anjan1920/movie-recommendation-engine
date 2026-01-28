# ---------------------------------------------------------------------
# -----How to Run-----                                                |
# run helper.py first to create user_item_matrix.csv                  |
# then run server.py to active server                                 |
# to run website go to the website's folder and type cmd              |
# in cmd type "python -m http.server" to expose HTTP on 8000 port     |
# then run wesbite by typing "http://localhost:8000/" in browser      |
# Recommended System will work only when there's 2 user in system     |
# -------------------------------------------------------------------


import os
from flask import Flask, jsonify , request
from flask_cors import CORS
import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

@app.route("/recommendation_system" , methods = ["POST"])
def recommendation_system():
    data = request.get_json()
    user_id = data.get('userID')
    liked_movies = data.get('likedMovies')
    print(user_id)
    print(liked_movies)

    df = pd.read_csv('imdb_top_1000.csv')
    indices = df[df["Series_Title"].isin(liked_movies)].index.tolist()
    print(indices)
    # print(df.loc[indices , "Series_Title"].tolist())
    df1 = pd.read_csv("user_item_matrix.csv")
    if user_id in df1['user_id'].values:
        row_index = df1[df1['user_id'] == user_id].index[0]
        for i in indices:
            df1.at[row_index, str(i)] = 1
    else:
        new_row = [0] * (df1.shape[1])
        new_row[0] = user_id
        for i in indices:
            new_row[i+1] = 1
        df1.loc[len(df1)] = new_row
    df1.to_csv("user_item_matrix.csv", index=False)
    recomended_movies = filter_movies(user_id , get_similar_users(user_id), 5)
    
    return jsonify({"status": "success", "recomended_movies": recomended_movies})



def get_similar_users(user_id):
    df = pd.read_csv('user_item_matrix.csv')
    user_ids = df['user_id'].values
    movie_matrix = df.drop(columns=['user_id']).values
    user_idx = np.where(user_ids == user_id)[0][0]
    target_vector = movie_matrix[user_idx].reshape(1, -1)
    similarities = cosine_similarity(target_vector, movie_matrix)[0]
    similar_users = [(user_ids[i], similarities[i]) for i in range(len(user_ids)) if i != user_idx]
    sorted_similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)
    sorted_user_ids = [user[0] for user in sorted_similar_users]
    print("Sorted user IDs based on cosine similarity (most similar first):")
    # print(sorted_user_ids)
    return sorted_user_ids



def filter_movies(user_id, recommended_users, recommend=5):
    user_item_matrix = pd.read_csv('user_item_matrix.csv')
    movie_data = pd.read_csv("imdb_top_1000.csv")
    if user_id not in user_item_matrix['user_id'].values:
        print(f"Error: User ID {user_id} not found in the matrix.")
        return []
    
    user_row = user_item_matrix[user_item_matrix['user_id'] == user_id]

    if user_row.empty:
        print(f"Error: No data found for user {user_id}.")
        return []
    
    user_watched_movies = set(user_row.drop(columns=['user_id']).columns[user_row.drop(columns=['user_id']).iloc[0] == 1])
    print(f"Movies already watched by user {user_id}: {user_watched_movies}")

    recommended_movies = list()
    recommendation_ids = list()

    for r_user_id in recommended_users:
        print(f"Processing user: {r_user_id}")

        if r_user_id not in user_item_matrix["user_id"].values:
            print(f"Warning: no data found for user: {r_user_id}")
            continue
        
        r_user_row = user_item_matrix[user_item_matrix['user_id'] == r_user_id]

        if r_user_row.empty:
            print(f"Data for user {r_user_id} not available")
            continue
        
        r_user_watched_movies = set(r_user_row.drop(columns=['user_id']).columns[r_user_row.drop(columns=['user_id']).iloc[0] == 1])
        print(f"Movies watched by user {r_user_id}: {r_user_watched_movies}")

        recommendation_ids = r_user_watched_movies - user_watched_movies
        recommendation_ids = list(recommendation_ids)
        recommendation_ids = [int(x) for x in recommendation_ids]

        recommended_movies.extend(movie_data.loc[recommendation_ids , 'Series_Title'].tolist())
        print(f"recommended movies: {recommended_movies}")

        if len(recommended_movies) >= recommend:
            print(f"Recommendation set has reached {recommend} movies. Stopping.")
            break

        # print(f"\nRecommended Movies (IDs): {recommended_movies}")
    return recommendation_ids


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)