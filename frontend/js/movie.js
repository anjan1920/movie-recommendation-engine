const API_BASE = "http://127.0.0.1:8000";

// ================= UTIL =================
function getQueryParam(key) {
  return new URLSearchParams(window.location.search).get(key);
}

// ================= GLOBAL STATE =================
const movieTitle = getQueryParam("title");
const userID = localStorage.getItem("userID");

let recommendationsLoaded = false;

console.log("[INIT] movieTitle:", movieTitle);
console.log("[INIT] userID:", userID);

init();

// ================= INIT =================
async function init() {
  if (!movieTitle) {
    console.error("[INIT] No movie title in URL");
    document.getElementById("movie-title").innerText = "Movie not found.";
    return;
  }

  await loadMovieDetails();
  await syncUserLikeState();
  attachLikeHandler();
}

// ================= USER STATE =================
async function syncUserLikeState() {
  try {
    const res = await fetch(
      `${API_BASE}/user/state?user_id=${userID}&movie_title=${encodeURIComponent(movieTitle)}`
    );

    if (!res.ok) throw new Error("User state fetch failed");

    const state = await res.json();
    toggleLikeUI(state.has_liked_current_movie);

    if (!recommendationsLoaded) {
      recommendationsLoaded = true;
      loadRecommendations();
    }

  } catch (err) {
    console.error("[STATE] ERROR:", err);
  }
}

// ================= MOVIE DETAILS =================
async function loadMovieDetails() {
  try {
    const res = await fetch(`${API_BASE}/movie?title=${encodeURIComponent(movieTitle)}`);
    if (!res.ok) throw new Error("Movie fetch failed");

    const movie = await res.json();

    document.getElementById("movie-title").innerText = movie.title;
    document.getElementById("movie-overview").innerText = movie.overview;
    document.getElementById("movie-rating").innerText = `IMDB⭐ ${movie.rating}`;
    document.getElementById("movie-year").innerText = `Year: ${movie.year}`;
    document.getElementById("movie-director").innerText = `Director: ${movie.director}`;
    document.getElementById("genres-container").innerText = `Genres: ${movie.genres}`;
    document.getElementById("movie-poster").src = movie.poster;

    await loadTrailer(movie.title);

  } catch (err) {
    console.error("[MOVIE] ERROR:", err);
    document.getElementById("movie-title").innerText = "Failed to load movie.";
  }
}

// ================= TRAILER =================
async function loadTrailer(title) {
  try {
    const res = await fetch(`${API_BASE}/movie/trailer?title=${encodeURIComponent(title)}`);
    const data = await res.json();

    if (!data.videoId) {
      document.getElementById("video-container").innerHTML = "<p>No trailer found.</p>";
      return;
    }

    document.getElementById("video-container").innerHTML = `
      <iframe
        class="w-full h-full"
        src="https://www.youtube.com/embed/${data.videoId}"
        frameborder="0"
        allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen>
      </iframe>
    `;

  } catch (err) {
    console.error("[TRAILER] ERROR:", err);
    document.getElementById("video-container").innerHTML = "<p>Failed to load trailer.</p>";
  }
}

// ================= LIKE / UNLIKE =================
function attachLikeHandler() {
  document.getElementById("like-btn").onclick = () => sendLikeAction(1);
  document.getElementById("unlike-btn").onclick = () => sendLikeAction(0);
}

async function sendLikeAction(action) {
  try {
    const res = await fetch(`${API_BASE}/user/action`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userID,
        movie_title: movieTitle,
        action: action
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Like failed");

    toggleLikeUI(action === 1);

    if (data.should_recommend && !recommendationsLoaded) {
      recommendationsLoaded = true;
      loadRecommendations();
    }

  } catch (err) {
    console.error("[LIKE] ERROR:", err);
  }
}

function toggleLikeUI(liked) {
  document.getElementById("like-btn").classList.toggle("hidden", liked);
  document.getElementById("unlike-btn").classList.toggle("hidden", !liked);
}

// ================= RECOMMENDATIONS =================
async function loadRecommendations() {
  try {
    const res = await fetch(`${API_BASE}/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userID,opened_movie :movieTitle })
    });

    if (!res.ok) throw new Error("Recommendation failed");

    const movies = await res.json();
    renderRecommendations(movies);

  } catch (err) {
    console.error("[RECO] ERROR:", err);
  }
}

// ================= RENDER =================
function renderRecommendations(movies) {
  const container = document.getElementById("recommendation-container");
  container.innerHTML = "";

  movies.forEach(movie => {
    const card = document.createElement("div");
    card.className = "bg-[#1a1a1a] p-4 rounded-xl cursor-pointer hover:scale-105 transition";

    card.innerHTML = `
      <img src="${movie.poster}" class="rounded mb-2" />
      <h3 class="font-bold">${movie.title}</h3>
      <p class="text-sm text-gray-400">⭐ ${movie.rating}</p>
    `;

    card.onclick = () => {
      window.location.href = `movie.html?title=${encodeURIComponent(movie.title)}`;
    };

    container.appendChild(card);
  });
}
