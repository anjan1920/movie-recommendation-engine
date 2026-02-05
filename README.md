# 🎬 Movie Recommendation Engine

A **hybrid movie recommendation web application** that delivers intelligent movie suggestions using:

* 🎯 **Context-aware cold start** (based on the movie being viewed)
* 🎭 **Genre-based recommendations** for low-interaction users
* 🤝 **Collaborative filtering** using cosine similarity for active users

Built with **Flask (Python backend)** and **Vanilla JS + Tailwind CSS (frontend)**.

---

## 🚀 Features

* Movie detail page with poster, overview, rating, year, director, genres
* Trailer fetching via backend (YouTube API)
* Like / Unlike movies
* User interaction stored in a **user–item matrix**
* Dynamic recommendations update after likes
* Genre browsing page
* Context-aware cold start recommendations

---

## 🧠 Recommendation Logic

The system uses a **3-stage hybrid recommendation strategy**:

| User State                      | Logic Used                      | Description                                                                                                        |
| ------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Cold Start (0 likes)**        | Context-based Genre Recommender | Uses the genre of the currently opened movie to recommend top-rated similar-genre movies with slight randomization |
| **Low Interaction (<10 likes)** | Genre-Based Personalization     | Recommends movies based on frequency of genres in liked movies                                                     |
| **Active User (≥10 likes)**     | Collaborative Filtering         | Uses cosine similarity between users in the user-item matrix                                                       |

---

## 🏗 System Architecture

**Frontend**

* HTML pages (`index.html`, `movie.html`, `genre.html`)
* Tailwind CSS
* Vanilla JavaScript

**Backend**

* Flask REST API
* Pandas for data handling
* scikit-learn for similarity computation
* CSV-based storage (IMDB dataset + user-item matrix)

---

## 📂 Project Structure

### Frontend

```
frontend/
│
├── pages/
│   ├── index.html
│   ├── movie.html
│   └── genre.html
│
├── js/
│   ├── api.js
│   ├── home.js
│   ├── movie.js
│   └── genre.js
│
└── src/
    ├── input.css
    └── output.css
```

### Backend

```
backend/
│
├── data/
│   ├── imdb_top_1000.csv
│   └── user_item_matrix.csv
│
├── recommender/
│   ├── recommend.py
│   ├── genre_recommender.py
│   ├── similarity.py
│   ├── matrix.py
│   └── validator.py
│
├── config.py
└── server.py
```

---

## 🛠 Tech Stack

**Backend**

* Python 3.12.1
* Flask 3.1.2
* flask-cors 6.0.1
* pandas 2.3.1
* numpy 2.2.6
* scipy 1.16.1
* scikit-learn 1.7.1
* requests 2.32.4
* joblib 1.5.1

**Frontend**

* HTML5
* Tailwind CSS
* JavaScript
* Node.js v22.17.1 (for Tailwind CLI)

---

## ▶ How to Run

### 1️⃣ Clone the repository

```bash
git clone <repo-url>
cd movie-recommendation-engine
```

---

### 2️⃣ Run Backend

```bash
cd backend
python server.py
```

Server runs on:

```
http://127.0.0.1:8000
```

---

### 3️⃣ Build Tailwind (Frontend)

```bash
cd frontend
npx @tailwindcss/cli -i ./src/input.css -o ./src/output.css --watch
```

Then open:

```
frontend/pages/index.html
```

---

## 🔌 API Endpoints

| Endpoint            | Method | Description                       |
| ------------------- | ------ | --------------------------------- |
| `/movie`            | GET    | Get movie details                 |
| `/movie/trailer`    | GET    | Get YouTube trailer video ID      |
| `/genres`           | GET    | Get all available genres          |
| `/get_genre_movies` | GET    | Get movies of a specific genre    |
| `/user/action`      | POST   | Like / Unlike a movie             |
| `/user/state`       | GET    | Get user liked count + like state |
| `/recommend`        | POST   | Get recommended movies            |

---

## 📊 Dataset

* **IMDB Top 1000 Movies Dataset**
* Used fields: `Series_Title`, `Genre`, `IMDB_Rating`, `Poster_Link`, etc.

---

## 🔮 Future Improvements

* User authentication
* Database storage (instead of CSV)
* Content-based vector embeddings
* Real-time popularity tracking
* Deployment to cloud

---

## 🧑‍💻 Author Anjan Das 
##Connect with me on [LinkedIn](https://www.linkedin.com)](https://www.linkedin.com/in/anjan-das-22b278236/)

Built as a full-stack machine learning + web systems project combining **recommendation algorithms** with **real web architecture**.



Just say.
