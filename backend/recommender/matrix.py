import os
import pandas as pd
from config import IMDB_PATH, MATRIX_PATH


def update_user_matrix(user_id, liked_movie):
    """
    Updates (or creates) a user row in the user-item matrix
    based on liked movie titles.
    """
    

    df_movies = pd.read_csv(IMDB_PATH)

    # load the user-item matrix
    if os.path.exists(MATRIX_PATH) and os.path.getsize(MATRIX_PATH) > 0:
        df_matrix = pd.read_csv(MATRIX_PATH)
        # ensure user_id type consistency
        df_matrix["user_id"] = df_matrix["user_id"].astype(type(user_id))
    else:
        print("user_item matrix is not created")
        print("creating user_item matrix ")
        # matrix not present ->create new one
        columns = ["user_id"]

        # remaining columns = movie indices
        for i in range(len(df_movies)):
            columns.append(str(i))

        df_matrix = pd.DataFrame(columns=columns)

    # Convert movie titles --> indices from IMDB dataset
    movie_indices = df_movies[
        df_movies["Series_Title"].isin(liked_movie)
    ].index.tolist()

    # check if user exists
    if user_id in df_matrix["user_id"].values:
        # Existing user
        print("User exists in the user_item matrix..")
        row_index = df_matrix[df_matrix["user_id"] == user_id].index[0]
    else:
        
        print("User not present in matrix {new user}")
        print("Creating new user row ")
        # New user -> initialize all movie columns as 0
        new_row = {col: 0 for col in df_matrix.columns}
        new_row["user_id"] = user_id 

        df_matrix = pd.concat(
            [df_matrix, pd.DataFrame([new_row])],
            ignore_index=True
        )
        row_index = df_matrix.index[-1] #last row is new user row

    # mark liked movies as 1 (do NOT reset others)
    print("Marking liked movies as 1 in matrix ") 
    for movie_id in movie_indices:
        df_matrix.at[row_index, str(movie_id)] = 1

    # enforce consistent user_id type before saving
    df_matrix["user_id"] = df_matrix["user_id"].astype(type(user_id))

    # save matrix
    print("Saving the user_item matrix.")
    df_matrix.to_csv(MATRIX_PATH, index=False)

    print("User_item matrix updated..")
    return None
