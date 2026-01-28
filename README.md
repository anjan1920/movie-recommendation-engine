
# 🎬 Movie Recommendation Engine

> End-to-end personalized movie recommendation system using collaborative filtering, built with Python and Flask, with a web interface for real-time user interaction.

---

##  Features

* Personalized movie recommendations
* User-based collaborative filtering
* Cosine similarity for user matching
* Ranking system for unseen movies
* Cold-start handling using genre-based fallback
* Real-time interaction through web interface

---

##  How It Works

1. User selects liked movies
2. System updates the **user–item interaction matrix**
3. Cosine similarity finds similar users
4. Weighted scores generate ranked movie recommendations
5. Results displayed instantly via web interface

---

## 🛠 Tech Stack

**Backend**

* Python
* Pandas
* NumPy
* Flask

**Recommendation Logic**

* Collaborative Filtering
* Cosine Similarity
* Sparse Matrix Handling

**Frontend**

* HTML
* Tailwind CSS
* JavaScript

---


## ⚙️ Installation & Run

```bash
git clone https://github.com/anjan1920/movie-recommendation-engine.git
cd movie-recommendation-engine
pip install -r requirements.txt
python app.py
```

Open browser at:

```
http://127.0.0.1:8000
```

---

## 📊 Challenges Addressed

* Sparse user–item interaction data
* Cold-start users
* Similarity computation optimization
* Modular system design

---
