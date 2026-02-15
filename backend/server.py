from config import SERVER_HOST, SERVER_PORT, DEBUG
from config import IMDB_PATH
from config import MAX_RECOMMENDATIONS,MIN_SIMILARITY_SCORE 
from config import MATRIX_PATH,YT_API_KEY

from recommender.validator import validate_request
from recommender.matrix import update_user_matrix
from recommender.similarity import get_similar_users
from recommender.genre_recommender import recommend_by_genre
from recommender.recommend import recommend_movies

import pandas as pd
import requests
import json
import random


from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Load datasets once
df_movies = pd.read_csv(IMDB_PATH)




@app.route("/movie/trailer", methods=["GET"])
def get_trailer():

    '''we suppose to receive the movie title in request 
    and using the yt url we fetch the videoID and return as response
    )'''
    print("[GET] Trailer hit...")
    title = request.args.get("title")

    if not title:
        return jsonify({"error": "title is required"}), 400

    print(f"Fetching trailer from YT for {title}")

    

    query = f"{title} trailer"
    #yt URL
    url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&q={query}&type=video&maxResults=1&key={YT_API_KEY}"
    )
    
    res = requests.get(url)

    if res.status_code != 200:
        print("YouTube API failed..")
        return jsonify({"error": "YouTube API failed !!"}), 500
    
    print("YouTube API fetched success")
    response = res.json()
    

    items = response.get("items", [])

    if not items:
        return {"error": "No results found"}, 404

    first_item = items[0]

    if first_item.get("id", {}).get("kind") != "youtube#video":
        return {"error": "First result is not a video"}, 400

    video_id = first_item["id"]["videoId"]

    print("Video ID:", video_id)



    print("Sending back response from /movie/trailer")
    return jsonify({"videoId": video_id})





@app.route("/user/action", methods=["POST"])
def handle_user_like_dislike():
    '''
    Here we handle user like and dislike 
    request body have movie title and action 0/1 dislike/like
    based on this we update the user_item matrix an
    '''

    print("[POST] handle user action hit..")

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    user_id = data.get("user_id")
    movie_title = data.get("movie_title")
    action = data.get("action")   # 1 = like, 0 = dislike


    print(f"user_id:{user_id} movie:{movie_title} action:{action}")

    if user_id is None or movie_title is None or action not in [0, 1]:
        return jsonify({"error": "Invalid payload"}), 400

    # find movie in dataset
    movie_row = df_movies[
        df_movies["Series_Title"].str.strip().str.lower()
        == movie_title.strip().lower()
    ]

    if movie_row.empty:
        return jsonify({"error": "Movie not found"}), 404

    movie_id = str(movie_row.index[0])

    #matrix update
    print("Updating user_item matrix  .")
    if action == 1:
        # LIKE  --> use matrix update(or create new user row if needed)
        update_user_matrix(user_id, [movie_title])
    else:
        # DISLIKE --> set column to 0 manually
        df_matrix = pd.read_csv(MATRIX_PATH)
        df_matrix["user_id"] = df_matrix["user_id"].astype(type(user_id))

        if user_id in df_matrix["user_id"].values:
            df_matrix.loc[df_matrix["user_id"] == user_id, movie_id] = 0
            df_matrix.to_csv(MATRIX_PATH, index=False)

    # reload matrix to compute liked_count
    
    df_matrix = pd.read_csv(MATRIX_PATH)
    df_matrix["user_id"] = df_matrix["user_id"].astype(type(user_id))

    user_row = df_matrix[df_matrix["user_id"] == user_id].drop(columns=["user_id"])
    liked_count = int(user_row.sum(axis=1).values[0])

    print(f"Liked count now: {liked_count}")
    print("Sending back response from /user/action")

    return jsonify({
        "status": "success",
        "liked_count": liked_count,
        "should_recommend": True
    })





@app.route("/movie", methods=["GET"])
def load_movie_details():
    '''
     The req contain the movies title 
     based on that we return the movies details using DB(df_movies)
    '''
    print("[GET] load movie details  hit..")
    movie_title = request.args.get("title")
    print("Movie title ",movie_title)

    if not movie_title:
        return jsonify({"error": "movie title is required"}), 400

    

    # Normalize title for safe matching
    movie_row = df_movies[
        df_movies["Series_Title"].str.strip().str.lower()
        == movie_title.strip().lower()
    ]

    if movie_row.empty:
        return jsonify({"error": "Movie not found"}), 404

    movie = movie_row.iloc[0]

    print("Sending back response from /movie")

    response = {
        "title": movie["Series_Title"],
        "poster": movie["Poster_Link"],
        "year": movie["Released_Year"],
        "rating": movie["IMDB_Rating"],
        "certificate": movie["Certificate"],
        "runtime": movie["Runtime"],
        "genres": movie["Genre"].split(", "),
        "director": movie["Director"],
        "overview": movie["Overview"]
    }

    return jsonify(response)




#home page
@app.route("/genres", methods=["GET"])
def get_genres():
    '''its hit when home pge loads
        and we have to  server the movie poster of the genres 

    '''
    print("[GET] load home page hits")
    # Extract unique genres from db
    genre_set = set()
    for g in df_movies["Genre"].dropna():
        for genre in g.split(","):
            genre_set.add(genre.strip())

    # Genre and  image mapping
    genreImages = {
        "Action": "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg",
        "Drama": "https://m.media-amazon.com/images/M/MV5BY2E1NDI5OWEtODJmYi00Nzg2LWI4MjUtODFiMTU2YWViOTU3XkEyXkFqcGc@._V1_.jpg",
        "Comedy": "https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_.jpg",
        "Horror": "https://m.media-amazon.com/images/M/MV5BMTM3NjA1NDMyMV5BMl5BanBnXkFtZTcwMDQzNDMzOQ@@._V1_.jpg",
        "Romance": "https://upload.wikimedia.org/wikipedia/en/1/18/Titanic_%281997_film%29_poster.png",
        "Adventure": "https://musicart.xboxlive.com/7/90a31100-0000-0000-0000-000000000002/504/image.jpg",
        "Crime": "https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_.jpg",
        "Biography": "https://m.media-amazon.com/images/M/MV5BN2JkMDc5MGQtZjg3YS00NmFiLWIyZmQtZTJmNTM5MjVmYTQ4XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        "History": "https://m.media-amazon.com/images/M/MV5BNjI3NjY1Mjg3MV5BMl5BanBnXkFtZTgwMzk5MDQ3MjE@._V1_.jpg",
        "Sci-Fi": "https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        "Fantasy": "https://m.media-amazon.com/images/M/MV5BNTU1MzgyMDMtMzBlZS00YzczLThmYWEtMjU3YmFlOWEyMjE1XkEyXkFqcGc@._V1_.jpg",
        "Thriller": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
        "Animation": "https://m.media-amazon.com/images/M/MV5BMTg5NzY0MzA2MV5BMl5BanBnXkFtZTYwNDc3NTc2._V1_FMjpg_UX1000_.jpg",
        "Family": "https://m.media-amazon.com/images/M/MV5BMjAwMzAzMzExOF5BMl5BanBnXkFtZTgwOTcwMDA5MTE@._V1_.jpg",
        "War": "https://m.media-amazon.com/images/M/MV5BMTkxNzI3ODI4Nl5BMl5BanBnXkFtZTgwMjkwMjY4MjE@._V1_FMjpg_UX1000_.jpg",
        "Mystery": "https://m.media-amazon.com/images/M/MV5BMTg0NjEwNjUxM15BMl5BanBnXkFtZTcwMzk0MjQ5Mg@@._V1_.jpg",
        "Music": "https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_.jpg",
        "Musical": "https://m.media-amazon.com/images/M/MV5BNTRlNmU1NzEtODNkNC00ZGM3LWFmNzQtMjBlMWRiYTcyMGRhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        "Sport": "https://i.pinimg.com/736x/74/64/2e/74642e61235070450a84ddde496aa1f3.jpg"
    }

    #response
    print("Sending back response from /genres")
    response = []
    for genre in sorted(genre_set):
        response.append({
            "genre": genre,
            "image": genreImages.get(genre)
        })

    return jsonify(response)






@app.route("/get_genre_movies", methods=["GET"])
def get_same_genre_movies():
    '''
    Here the req have the specific genre
    based on that genre we have to server the movies 
    '''
    print("[GET] get same genre movies hit..")
    selected_genre = request.args.get("genre")
    print(" User click genre ",selected_genre)

    if not selected_genre:
        return jsonify({"error": "genre is required"}), 400


    movies = df_movies[df_movies["Genre"].str.contains(selected_genre, case=False, na=False)]

    response = movies[
        #each movie contain this info
        [
        "Series_Title",
        "Poster_Link",
        "IMDB_Rating",
        "Released_Year",
        "Genre"
    ]
    ].to_dict(orient="records")
    print("Sending back response from  /get_genre_movies")

    return jsonify(response)






@app.route("/user/state", methods=["GET"])
def user_like_state():
    '''we  received the user id and current open movie 
    and have to return the user_like state 
    i.e which movies uer liked so far
    '''
    print("[GET] get user state hit..")
    

    try:
        user_id = request.args.get("user_id")
        movie_title = request.args.get("movie_title")

        if not user_id or not movie_title:
            return jsonify({"error": "Missing user_id or movie_title"}), 400
        print(f"User id {user_id} Opened movie {movie_title}")

        df_matrix = pd.read_csv(MATRIX_PATH)
        # Check user exists
        if user_id not in df_matrix["user_id"].values:
            print("User is not in user_item matrix {did not like any  movie yet}")
            # New user --> no likes yet
            return jsonify({
                "liked_count": 0,
                "has_liked_current_movie": False
            })

        
        # Get user row
        user_row = df_matrix[df_matrix["user_id"] == user_id].iloc[0]
        # Count total liked movies
        liked_count = int(user_row.drop("user_id").sum())

        # Check if current movie is liked
        movie_match = df_movies[
            df_movies["Series_Title"].str.strip() == movie_title.strip()
        ]

        has_liked_current_movie = False

        if not movie_match.empty:
            movie_index = str(movie_match.index[0])  # column name as string

            if movie_index in user_row.index:
                has_liked_current_movie = user_row[movie_index] == 1
        print("like count :",liked_count)
        # Response
        print("Sending back response from  /user/state")
        return jsonify({
            "liked_count": liked_count,
            "has_liked_current_movie": bool(has_liked_current_movie)
        })
    

    except Exception as e:
        print("[USER STATE ERROR]", e)
        return jsonify({"error": "Internal server error"}), 500







@app.route("/recommend", methods=["POST"])
def recommend():
    '''Here the get the user id
        based on that our target is to recommend movies 
    '''

    print("[POST] recommend Request hit..")
    if not request.is_json:
        print("400,Not a json request...")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # now validate the json data
    print("Validating request...")
    valid, error = validate_request(data, df_movies)
    if not valid:
        print(f"Invalid request ,ERR{error}")
        return jsonify({"error": error}), 400
    print("Request validation successful..")

    # extract user id
    user_id = data["user_id"]
    print(f"User id :{user_id}")
    opened_movie = data['opened_movie']

    # load matrix
    df_matrix = pd.read_csv(MATRIX_PATH)

    # check if user exists in matrix
    user_row = df_matrix[df_matrix["user_id"] == user_id]

    liked_movies = []
    liked_count = 0
   
    if not user_row.empty:
        print("User exists on user_item matrix ..")
        # get liked movie ids (columns marked 1)
        liked_cols = user_row.drop("user_id", axis=1)
        liked_movie_ids = liked_cols.loc[:, (liked_cols == 1).any()].columns.tolist()

        # convert movie ids to titles
        liked_movies = df_movies.loc[
            df_movies.index.astype(str).isin(liked_movie_ids),
            "Series_Title"
        ].tolist()

        liked_count = len(liked_movies)

    print(f"Liked count : {liked_count}")
    print("User count : ",(df_matrix.shape)[0])
    user_count = (df_matrix.shape)[0]

    # Recommendation decision 
    #cold start
    if liked_count == 0:
        print("Cold start user --> genre-based recommendation using opened movie")

        movie_row = df_movies[
            df_movies["Series_Title"].str.strip().str.lower()
            == opened_movie.strip().lower()
        ]

        if movie_row.empty:
            print("Opened movie not found -> fallback to global top rated")
            recommended_titles = df_movies.sort_values(
                "IMDB_Rating", ascending=False
            )["Series_Title"].head(10).tolist()

        else:
            print("Opened movie found -> recommending same genre top rated (with variation)")

            # extract primary genre only
            base_genres = []
            for g in movie_row.iloc[0]["Genre"].split(","):
                base_genres.append(g.strip())
            base_genres = base_genres[:1]   # keep primary genre
            print("Current movie based genres:", base_genres)

            genre_movies = []

            # collect movies with same primary genre
            for _, row in df_movies.iterrows():
                title = row["Series_Title"]

                if title == opened_movie:
                    continue

                movie_genres = [g.strip() for g in row["Genre"].split(",")]

                if any(g in base_genres for g in movie_genres):
                    genre_movies.append((title, row["IMDB_Rating"]))

            # sort by rating (quality first)
            genre_movies.sort(key=lambda x: x[1], reverse=True)

            # take a high-quality pool (top 30)
            top_pool = genre_movies[:30]

            # randomize selection inside that pool
            random.shuffle(top_pool)

            # final recommendation list
            recommended_titles = [title for title, _ in top_pool[:15]]

        print("Recommended titles:", recommended_titles)


    elif liked_count < 10 or user_count < 5: 
        print("Low interaction user ->  genre based recommendation")
        recommended_titles = recommend_by_genre(liked_movies, top_n=10)

    else:
        print("Mature user -> collaborative filtering")
        similar_users = get_similar_users(user_id, MIN_SIMILARITY_SCORE, MAX_RECOMMENDATIONS)
        recommended_titles = recommend_movies(user_id, similar_users, 5)

    print(f"Recommended titles : {recommended_titles}")

    #Convert titles to full movie objects for frontend 

    response_movies = []

    for title in recommended_titles:
        movie_row = df_movies[df_movies["Series_Title"] == title]
        if movie_row.empty:
            continue

        movie_row = movie_row.iloc[0]

        response_movies.append({
            "title": movie_row["Series_Title"],
            "rating": movie_row["IMDB_Rating"],
            "poster": movie_row["Poster_Link"]  # adjust if column name differs
        })
    print("Sending back response from /recommend")

    return jsonify(response_movies)







if __name__ == "__main__":
    print(f"Server is running on port:{SERVER_PORT}")
    app.run(
        
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=DEBUG,
       
    )