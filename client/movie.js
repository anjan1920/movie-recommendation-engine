function getQueryParam(key) {
    return new URLSearchParams(window.location.search).get(key);
}

const movieTitle = getQueryParam("title");

Papa.parse("imdb_top_1000.csv", {
    download: true,
    header: true,
    complete: (results) => {
        const movies = results.data.filter(m => m.Series_Title);
        const movie = movies.find(m => m.Series_Title.trim() === movieTitle);

        if (!movie) {
            document.getElementById("movie-title").innerText = "Movie not found.";
            return;
        }

        // document.getElementById("movie-title").innerText = movie.Series_Title;
        // document.getElementById("movie-rating").innerText = `Rating: ${movie.IMDB_Rating} | Year: ${movie.Released_Year}`;
        // document.getElementById("movie-overview").innerText = movie.Overview || "No description available.";
        // document.getElementById("movie-director").innerText = `Director: ${movie.Director}` || "No Director Names";
        // document.getElementById("movie-stars").innerText = `Stars: ${movie.Star1} • ${movie.Star2}` || "No Director Names";

        document.getElementById("info-section").innerHTML = `
            <h1 id="movie-title"><b>${movie.Series_Title}</b></h1>
            <p id="movie-year-certificate-runtime">${movie.Released_Year} • ${movie.Certificate} • ${movie.Runtime}</p>
            <div id = "genres-container"></div>
            <p id="movie-overview">${movie.Overview}</p><hr>
            <p id="movie-rating"><b>Rating: </b><i class="ri-star-fill rating-icon"></i> ${movie.IMDB_Rating}/10 | <b>Year:</b> ${movie.Released_Year}</p><hr>
            <p id="movie-director"><b>Director </b><i>${movie.Director}</i></p><hr>
            <p id="movie-stars"><b>Stars </b><i>${movie.Star1} • ${movie.Star2} • ${movie.Star3} • ${movie.Star4}</i></p>`;

        let genres = movie.Genre.split(',').map(g => g.trim());
        genres_container = document.getElementById("genres-container");
        genres.forEach(genre => {
            const tile = document.createElement("div");
            tile.className = "genre-tile";
            tile.innerText = genre;
            tile.onclick = () => {
                window.location.href = `genre.html?genre=${encodeURIComponent(genre)}`;
            }

            genres_container.appendChild(tile);
        });


        const searchQuery = encodeURIComponent(`${movie.Series_Title} trailer`);
        console.log(movie.Series_Title)

        fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&q=${searchQuery}&key=AIzaSyAAAbiNdyky0Rek9O2xhPHvrRuItYlZr7M&type=video&maxResults=1`)
            .then(res => res.json())
            .then(data => {
                if (data.items.length === 0) {
                    document.getElementById("video-container").innerHTML = `<p>No trailer found.</p>`;
                    return;
                }

                const videoId = data.items[0].id.videoId;
                const youtubeEmbed = `
                    <iframe 
                        src="https://www.youtube.com/embed/${videoId}"
                        frameborder="0" 
                        allow="autoplay; encrypted-media" 
                        allowfullscreen>
                    </iframe>`;

                document.getElementById("video-container").innerHTML = youtubeEmbed;
            })
            .catch(err => {
                console.error("YouTube API error:", err);
                document.getElementById("video-container").innerHTML = `<p>Failed to load trailer.</p>`;
            });
    }
});

let recommendedMovies = [];
let likedMovies = JSON.parse(localStorage.getItem("likedMovies")) || [];

function renderRecommendationSystem() {
    let container = document.getElementById("recommendation-container");
    console.log(recommendedMovies[1])
    recommendedMovies.forEach(movieID => {
        Papa.parse("imdb_top_1000.csv", {
            download: true,
            header: true,
            complete: function (results) {
                const data = results.data;
                let movie = data[movieID];
                let card = document.createElement("div");
                card.className = "movie-card";
                card.innerHTML = `
                    <img src="${movie.Poster_Link}" alt="${movie.Series_Title}" draggable="false"/>
                    <div class = "movie-card-details">
                        <h1>${movie.Series_Title}</h1>
                        <p><b>Rating: </b><i class="ri-star-fill rating-icon"></i>${movie.IMDB_Rating}/10</p>
                    </div>`;
                card.addEventListener('click', () => {
                    if (!likedMovies.includes(movie.Series_Title)) {
                        likedMovies.push(movie.Series_Title);
                        localStorage.setItem("likedMovies", JSON.stringify(likedMovies));
                        alert(`${movie.Series_Title} added`);
                    }
                    window.location.href = `movie.html?title=${encodeURIComponent(movie.Series_Title)}`;
                });

                container.appendChild(card);
            }
        });
    });
}

function recommendationSystem() {
    let userID = localStorage.getItem("userID");
    let likedMovies = JSON.parse(localStorage.getItem("likedMovies") || "[]");

    fetch("http://192.168.1.2:8000/recommendation_system", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            userID: userID,
            likedMovies: likedMovies
        })
    })
    .then(response => response.json())
    .then(data => {
        const movies = data.recomended_movies;
        console.log("movies: ",movies);
        recommendedMovies.push(...movies);
        renderRecommendationSystem();
    })
    .catch(error => {
        console.log("Error sending data to server", error);
    });
}
recommendationSystem()
// renderRecommendationSystem();