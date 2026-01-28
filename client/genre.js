function getQueryParams(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

selectedGenre = getQueryParams("genre");
document.getElementById("genre-title").innerText = `Genre: ${selectedGenre}`;

let genreMovies = [];
let filteredMovies = [];
let likedMovies = JSON.parse(localStorage.getItem("likedMovies")) || [];

Papa.parse("imdb_top_1000.csv", {
    download: true,
    header: true,
    complete: (results) => {
        const movies = results.data.filter(m => m.Series_Title && m.Genre);
        genreMovies = movies.filter(movie => movie.Genre.split(',').map(g => g.trim()).includes(selectedGenre));

        const container = document.getElementById("movie-container");

        if (genreMovies.length === 0) {
            container.innerHTML = "<p>No movies found for this genre.</p>";
            return;
        }
        renderMovies(genreMovies);
    }
});

document.getElementById("searchbar-text").addEventListener('input', applyFilters);
document.getElementById("rating-text").addEventListener('input', applyFilters);
document.getElementById("year-text").addEventListener('input', applyFilters);

function applyFilters() {
    const searchText = document.getElementById('searchbar-text').value.toLowerCase();
    const minRating = parseFloat(document.getElementById('rating-text').value);
    const minYear = parseInt(document.getElementById('year-text').value);

    filteredMovies = genreMovies.filter(movie => {
        const titleMatch = !searchText || movie.Series_Title.toLowerCase().includes(searchText);
        const ratingMatch = isNaN(minRating) || parseFloat(movie.IMDB_Rating) >= minRating;
        const yearMatch = isNaN(minYear) || parseInt(movie.Released_Year) >= minYear;

        return titleMatch && ratingMatch && yearMatch;
    });

    renderMovies(filteredMovies);
}

function renderMovies(movieList) {
    console.log(likedMovies);
    const container = document.getElementById("movie-container");
    container.innerHTML = "";

    if (movieList.length === 0) {
        container.innerHTML = "<p>No movies found for this genre.</p>";
        return;
    }

    movieList.forEach(movie => {
        const card = document.createElement("div");
        card.className = "movie-card";
        card.innerHTML = `
            <img src="${movie.Poster_Link}" alt="${movie.Series_Title}" draggable="false"/>
            <h3>${movie.Series_Title}</h3>
            <p>Rating: ${movie.IMDB_Rating}</p>
            <p>Year: ${movie.Released_Year}</p>
            <p>Genre: ${movie.Genre}</p>`;
        card.onclick = () => {
            if(!likedMovies.includes(movie.Series_Title))
            {
                likedMovies.push(movie.Series_Title);
                localStorage.setItem("likedMovies" , JSON.stringify(likedMovies));
                alert(`${movie.Series_Title} added`);
            }
            window.location.href = `movie.html?title=${encodeURIComponent(movie.Series_Title)}`;
        }
        container.appendChild(card);
    });
}