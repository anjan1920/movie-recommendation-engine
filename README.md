# 🎬 Movie Recommendation System

A progressive movie recommendation system built using  **Flask, Pandas, NumPy, and Scikit-learn** , implementing a staged personalization strategy from cold-start to collaborative filtering.

---

## 🚀 Project Overview

This system provides personalized movie recommendations using a  **3-stage recommendation strategy** :

1. **Cold Start (No Interaction)**
2. **Genre-Weighted Recommendation (Low Interaction Users)**
3. **User-User Collaborative Filtering (Mature Users)**

The recommendation engine improves as user interaction increases.

---

## ✨ Features

* User-based Collaborative Filtering (Cosine Similarity)
* Genre-weighted recommendation for sparse interaction
* Cold-start handling
* Real-time like/dislike updates
* Dynamic frontend using HTML + Tailwind CSS
* YouTube trailer integration
* Configurable thresholds via `config.py`
* CSV-based user-item persistence

---

## 🏗️ System Architecture

Frontend (HTML + JS)
↓
Flask API Layer
↓
Recommendation Engine
↓
User-Item Matrix (CSV Storage)

All recommendation logic is handled on the backend.

---

## 🧠 Recommendation Strategy

### 🔹 Stage 1 – Cold Start

If the user has 0 liked movies:

* Recommend top-rated movies from selected genre.

---

### 🔹 Stage 2 – Genre-Based Heuristic

If user interaction is low OR total users < 5:

* Analyze genres of liked movies.
* Count genre frequency.
* Score unseen movies based on genre overlap.
* Recommend highest scored movies.

This avoids unreliable similarity computation in sparse data.

---

### 🔹 Stage 3 – Collaborative Filtering

If user has enough interaction and sufficient user base:

* Build user-item matrix (1 = liked, 0 = not liked)
* Compute cosine similarity between users
* Select top similar users
* Aggregate similarity scores
* Recommend highest scored unseen movies

Cosine similarity formula:

```
cos(A, B) = (A · B) / (|A| × |B|)
```

---

## 🛠️ Tech Stack

### Backend

* Python 3.12+
* Flask
* Flask-CORS
* Pandas
* NumPy
* Scikit-learn
* Requests

### Frontend

* HTML
* Tailwind CSS
* JavaScript

### External API

* YouTube Data API (for trailer integration)---
* 

## 📂 Project Structure

backend/
  ├── server.py
  ├── config.py
  ├── recommender/
  └── data/

frontend/
  ├── pages/
  └── js/

---
 Setup & Installation
---------------------

### Recommended Python Version: 3.12+

### 1️⃣ Clone the Repository

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   git clone https://github.com/anjan1920/movie-recommendation-engine  cd movie-recommendation-engine   `

### 2️⃣ Backend Setup (Python + Flask)

#### Create Virtual Environment (Recommended)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m venv venv   `

Activate:

Windows:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   venv\Scripts\activate   `

Mac/Linux:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   source venv/bin/activate   `

#### Install Dependencies

If requirements.txt exists:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

If not, install manually:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install flask pandas numpy requests   `


--
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

Understanding the developer guide will help you modify the system safely.

---
