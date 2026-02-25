

---

# 📘 Developer Guide – Movie Recommendation System

---

## 1. Project Purpose

This project implements a progressive movie recommendation system.

The system improves personalization step by step:

* Stage 1 → Cold start (no user data)
* Stage 2 → Genre-weighted recommendation
* Stage 3 → User-user collaborative filtering

The goal is to provide meaningful recommendations even when user data is limited.

---

## 2. High-Level Flow

The system follows a request–response architecture where the frontend triggers API calls and the backend handles all recommendation logic.

---

### Step 1: User Visits Home Page

* When the home page loads, a `user_id` is generated using JavaScript.
* This `user_id` is stored in browser local storage.
* No authentication system is used; this ID tracks user interaction locally.

---

### Step 2: Load Genres

Frontend calls:

```
GET /genres
```

Backend:

* Extracts available genres from dataset
* Returns genre names + poster links

Frontend:

* Dynamically renders clickable genre tiles

---

### Step 3: Genre Selection

When user clicks a genre:

Frontend calls:

```
GET /get_genre_movies?genre=<selected_genre>
```

Backend:

* Filters dataset by genre
* Returns movies of that genre (title, rating, poster, etc.)

Frontend:

* Displays filtered movies
* Allows optional client-side filtering (year, rating)

---

### Step 4: Movie Detail Page

When user selects a movie:

Frontend calls:

```
GET /movie?title=<movie_title>
```

Backend:

* Returns full movie details
* Fetches trailer video ID using YouTube API
* Sends trailer ID to frontend

Frontend:

* Displays movie details
* Embeds trailer using iframe

At this stage, recommendation logic is also triggered.

---

### Step 5: Check User State

Frontend calls:

```
GET /user/state?user_id=...&movie_title=...
```

Backend returns:

* Total number of liked movies
* Whether current movie is already liked

This helps determine which recommendation stage to apply.

---

### Step 6: Generate Recommendation

Frontend calls:

```
POST /recommend
```

Backend decides recommendation strategy based on:

* If `user_like_count == 0`
  → Stage 1 (Cold Start)
* If `user_like_count < threshold`
  OR total users < 5
  → Stage 2 (Genre-weighted heuristic)
* If `user_like_count >= threshold`
  AND total users > 5
  → Stage 3 (Collaborative filtering)

All recommendation logic runs on the backend.
Frontend only displays returned results.

---

### Step 7: Like / Dislike Action

When user clicks like/dislike:

Frontend calls:

```
POST /user/action
```

Backend:

* Updates user-item matrix
* Saves updated matrix to CSV
* Returns updated like count
* Returns `should_recommend` flag

If `should_recommend = true`,
Frontend re-triggers `/recommend`.

---

## 3. Recommendation Strategy

The system uses a  **3-stage progressive recommendation approach** .

---

### Stage 1 – Cold Start

**Condition:**

* User has 0 liked movies

**Logic:**

* Recommend top-rated movies from selected genre

**Purpose:**

* Basic recommendation without personalization

---

### Stage 2 – Low Interaction User (Genre-Based Heuristic)

**Condition:**

* User liked few movies (below threshold)
* OR total users in system < 5

**Why:**
Collaborative filtering is unreliable with sparse user data.

**Logic:**

1. Get all liked movies of current user
2. Extract genres from those movies
3. Count genre frequency
4. Assign weight to each genre
5. Score unseen movies based on genre overlap

**Example:**

User liked:

* Action (3)
* Sci-Fi (2)
* Thriller (1)

Movie with:

* Action + Sci-Fi
  → Score = 3 + 2 = 5

Sort by score and return top results.

This method does not depend on other users.

---

### Stage 3 – Collaborative Filtering (Mature User)

**Condition:**

* User has enough liked movies
* Total users > 5

Now similarity between users becomes meaningful.

---

#### Step 1: User-Item Matrix

Matrix structure:

* Rows → Users
* Columns → Movies
* Value = 1 (liked), 0 (not liked)

Example:

| user_id | movie_A | movie_B | movie_C |
| ------- | ------- | ------- | ------- |
| user_1  | 1       | 1       | 0       |
| user_2  | 0       | 1       | 0       |
| user_3  | 1       | 1       | 1       |

Matrix stored in:

```
data/user_item_matrix.csv
```

---

#### Step 2: Cosine Similarity

Each user row is treated as a vector.

Similarity formula:

```
cos(A, B) = (A · B) / (|A| × |B|)
```

* Dot product → common liked movies
* Magnitude → normalization
* Output → similarity score (0 to 1)

Only users with similarity > `MIN_SIMILARITY_SCORE` are considered.

---

#### Step 3: Select Top Similar Users

* Sort users by similarity
* Select top N users
* Ignore self

---

#### Step 4: Generate Recommendation Scores

For each similar user:

* Get movies they liked
* Exclude movies already liked by current user
* Add similarity score to movie score

**Example:**

If:

* user_A similarity = 0.8
* user_B similarity = 0.6

Both liked Movie_X

Score(Movie_X) = 0.8 + 0.6 = 1.4

Sort by score → return top results.

---

## 4. User Action & Matrix Update

Endpoint:

```
POST /user/action
```

Request contains:

* user_id
* movie_title
* action (1 = like, 0 = dislike)

If like:

* Update user_item matrix
* Create new row if user not present

Matrix is saved to CSV for persistence.

If enough new interaction:

* `should_recommend = true`
* Recommendation recalculated

---

## 5. API Endpoints Overview

### GET /genres

Returns genre list + poster

### GET /get_genre_movies

Returns movies for a specific genre

### GET /movie

Returns full movie details

### GET /user/state

Returns:

* Total liked movies
* Whether current movie is liked

### POST /recommend

Triggers recommendation logic (Stage 1, 2, or 3)

### POST /user/action

Updates matrix and interaction state

### GET /movie/trailer

Fetches trailer video ID using YouTube API

---

## 6. Setup & Installation

### Recommended Python Version: 3.12+

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/anjan1920/movie-recommendation-engine
cd movie-recommendation-engine
```

---

### 2️⃣ Backend Setup (Python + Flask)

#### Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

---

#### Install Dependencies

If `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

If not, install manually:

```bash
pip install flask pandas numpy requests
```

---

### 3️⃣ Dataset Setup

Inside the `data/` directory, ensure:

* `imdb_top_1000.csv` exists
* `user_item_matrix.csv` exists (can be empty initially)

If matrix file does not exist:

* System can create it dynamically on first user interaction.

---

### 4️⃣ Configuration Setup (`config.py`)

All configurable values are stored inside:

```
backend/config.py
```

Important fields:

```python
IMDB_PATH
MATRIX_PATH
MAX_LIKED_MOVIES
MAX_RECOMMENDATIONS
MIN_SIMILARITY_SCORE
SERVER_HOST
SERVER_PORT
DEBUG
YT_API_KEY
```

---

### 5️⃣ Frontend Setup

No separate build step required.

Frontend files are located in:

```
frontend/pages
```

In VS Code, open `index.html` using  **Live Server** .

---

### 6️⃣ First-Time Behavior

When first user interacts:

* `user_id` is generated automatically
* `user_item_matrix.csv` may be updated
* Recommendations initially use Cold Start logic

System progressively improves as more interactions happen.

---

## 7. Possible Improvements

* Use PostgreSQL instead of CSV
* Use sparse matrix representation
* Precompute similarity matrix
* Switch to item-based CF
* Use matrix factorization (SVD)
* Add JWT authentication
* Add Redis caching
