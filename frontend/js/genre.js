

const API_BASE = "http://127.0.0.1:8000";

let allMovies = [];     // full list from server
let filteredMovies = []; // after filters


//entry point
init();

function init() {
    //get the genre form calling page
  const genre = getGenreFromURL();

  if (!genre) {
    alert("Genre not found");
    window.location.href = "index.html";
    return;
  }

  setGenreTitle(genre);
  fetchGenreMovies(genre);
  attachFilterListeners();
}


function getGenreFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("genre");
}

function setGenreTitle(genre) {
  document.getElementById("genre-title").innerText = `Genre: ${genre}`;
}

///server call
async function fetchGenreMovies(genre) {
  showLoading(true);

  try {
    const res = await fetch(
      `${API_BASE}/get_genre_movies?genre=${encodeURIComponent(genre)}`
    );

    if (!res.ok) throw new Error("Server error");

    allMovies = await res.json();
    filteredMovies = allMovies;

    renderMovies(filteredMovies);

  } catch (err) {
    showError("Failed to load movies");
    console.error(err);
    
  } finally {
    showLoading(false);
  }
}

//ui update 
function renderMovies(movies) {
  const container = document.getElementById("movie-container");
  container.innerHTML = "";

  if (!movies.length) {
    container.innerHTML = "<p>No movies found.</p>";
    return;
  }

  movies.forEach(movie => {
    const card = document.createElement("div");
    card.className = `
    bg-[#1a1a1a]
    w-[240px]
    rounded-2xl
    p-5
    cursor-pointer

    transition-all duration-300 ease-out
    hover:scale-105

    shadow-[0_0_15px_rgba(0,255,150,0.15)]
    hover:shadow-[0_0_30px_rgba(0,255,150,0.35)]
    `;


    card.innerHTML = `
      <img src="${movie.Poster_Link} " class="w-full h-52 object-fill rounded-lg mb-3"/>

      <h3 class="font-bold">${movie.Series_Title}</h3>
      <p class="text-sm text-gray-400">⭐ ${movie.IMDB_Rating}</p>
      <p class="text-sm text-gray-400">${movie.Released_Year}</p>
    `;

    card.onclick = () => {
      window.location.href =
        `movie.html?title=${encodeURIComponent(movie.Series_Title)}`;
    };

    container.appendChild(card);
  });
}

//filter 
function attachFilterListeners() {
  document.getElementById("searchbar-text")?.addEventListener("input", applyFilters);
  document.getElementById("rating-text")?.addEventListener("input", applyFilters);
  document.getElementById("year-text")?.addEventListener("input", applyFilters);
}

function applyFilters() {
  const search = document.getElementById("searchbar-text").value.toLowerCase();
  const minRating = parseFloat(document.getElementById("rating-text").value);
  const minYear = parseInt(document.getElementById("year-text").value);

  filteredMovies = allMovies.filter(m => {
    const titleMatch =
      !search || m.Series_Title.toLowerCase().includes(search);
    const ratingMatch =
      isNaN(minRating) || parseFloat(m.IMDB_Rating) >= minRating;
    const yearMatch =
      isNaN(minYear) || parseInt(m.Released_Year) >= minYear;

    return titleMatch && ratingMatch && yearMatch;
  });

  renderMovies(filteredMovies);
}


function showLoading(show) {
  // optional: toggle loading text / spinner
}

function showError(msg) {
  alert(msg);
}

