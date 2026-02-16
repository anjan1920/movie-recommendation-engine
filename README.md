# 🎬 Movie Recommendation System

A progressive movie recommendation system built using **Flask, Pandas, NumPy, and Scikit-learn**, implementing a staged personalization strategy from cold-start to collaborative filtering.

---

## 🚀 Project Overview

This system provides personalized movie recommendations using a **3-stage recommendation strategy**:

1. **Cold Start (No Interaction)**
2. **Genre-Weighted Recommendation (Low Interaction Users)**
3. **User-User Collaborative Filtering (Mature Users)**

The recommendation engine improves dynamically as user interaction increases.

---

## ✨ Features

* ✅ User-based Collaborative Filtering (Cosine Similarity)
* ✅ Genre-weighted recommendation for sparse interaction
* ✅ Cold-start handling
* ✅ Real-time like/dislike updates
* ✅ Dynamic frontend using HTML + Tailwind CSS
* ✅ YouTube trailer integration
* ✅ Configurable thresholds via `config.py`
* ✅ CSV-based user-item persistence

---

## 🏗️ System Architecture

```
Frontend (HTML + JS)
        ↓
Flask API Layer
        ↓
Recommendation Engine
        ↓
User-Item Matrix (CSV Storage)
```

All recommendation logic is handled on the backend.

---

## 🧠 Recommendation Strategy

### 🔹 Stage 1 – Cold Start

If the user has **0 liked movies**:

* Recommend top-rated movies from selected genre.

---

### 🔹 Stage 2 – Genre-Based Heuristic

If user interaction is low **OR** total users < 5:

* Analyze genres of liked movies
* Count genre frequency
* Score unseen movies based on genre overlap
* Recommend highest scored movies

This avoids unreliable similarity computation in sparse data.

---

### 🔹 Stage 3 – Collaborative Filtering

If user has enough interaction and sufficient user base:

* Build user-item matrix (1 = liked, 0 = not liked)
* Compute cosine similarity between users
* Select top similar users
* Aggregate similarity scores
* Recommend highest scored unseen movies

**Cosine Similarity Formula:**

```
cos(A, B) = (A · B) / (|A| × |B|)
```

---

## 🛠️ Tech Stack

### 🔹 Backend

* Python 3.12+
* Flask
* Flask-CORS
* Pandas
* NumPy
* Scikit-learn
* Requests

### 🔹 Frontend

* HTML
* Tailwind CSS
* JavaScript

### 🔹 External API

* YouTube Data API (Trailer Integration)

---

## 📂 Project Structure

```
backend/
  ├── server.py
  ├── config.py
  ├── recommender/
  └── data/

frontend/
  ├── pages/
  └── js/
```

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/anjan1920/movie-recommendation-engine.git
cd movie-recommendation-engine
```

---

## ⚙️ Backend Setup (Python + Flask)

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

**🪟 Windows**

```bash
venv\Scripts\activate
```

**🍎 Mac/Linux**

```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

If `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

If not:

```bash
pip install flask pandas numpy scikit-learn flask-cors requests
```

---

# ▶️ How to Run the Project

## 🔹 Run Backend Server

Navigate to backend folder:

```bash
cd backend
```

Start the server:

```bash
python server.py
```

Backend runs at:

```
http://127.0.0.1:8000/
```

---

## 🔹 Run Frontend

1. Open the project in **VS Code**
2. Navigate to:

```
frontend/pages
```

3. Right-click on `index.html`
4. Click **"Open with Live Server"**

The frontend will open automatically in your browser.

---

# 👨‍💻 Developer Note

If you are here to extend, optimize, or build on top of this system:

👉 Please read `DEVELOPER_GUIDE.md` first.

It explains:

* Internal architecture
* Recommendation logic in detail
* Matrix handling
* Threshold design decisions
* Full setup guide
* Extension strategies

Understanding the developer guide will help you modify the system safely and efficiently.


