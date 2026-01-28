Papa.parse("imdb_top_1000.csv", {
  download: true,
  header: true,
  complete: function (results) {
    const data = results.data.filter(m => m.Genre && m.Series_Title);
    const genreSet = new Set();

    data.forEach(movie => {
      const genres = movie.Genre.split(',').map(g => g.trim());
      genres.forEach(g => genreSet.add(g));
    });

    const genreContainer = document.getElementById("genre-container");

    const genreImages = {
      Action: 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg',
      Drama: 'https://m.media-amazon.com/images/M/MV5BY2E1NDI5OWEtODJmYi00Nzg2LWI4MjUtODFiMTU2YWViOTU3XkEyXkFqcGc@._V1_.jpg',
      Comedy: 'https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_.jpg',
      Horror: 'https://m.media-amazon.com/images/M/MV5BMTM3NjA1NDMyMV5BMl5BanBnXkFtZTcwMDQzNDMzOQ@@._V1_.jpg',
      Romance: 'https://upload.wikimedia.org/wikipedia/en/1/18/Titanic_%281997_film%29_poster.png',
      Adventure: 'https://musicart.xboxlive.com/7/90a31100-0000-0000-0000-000000000002/504/image.jpg',
      Crime: 'https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_.jpg',
      Biography: 'https://m.media-amazon.com/images/M/MV5BN2JkMDc5MGQtZjg3YS00NmFiLWIyZmQtZTJmNTM5MjVmYTQ4XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
      History: 'https://m.media-amazon.com/images/M/MV5BNjI3NjY1Mjg3MV5BMl5BanBnXkFtZTgwMzk5MDQ3MjE@._V1_.jpg',
      'Sci-Fi': 'https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
      Western: 'https://m.media-amazon.com/images/M/MV5BMTU3MjUwMzQ3MF5BMl5BanBnXkFtZTgwMjcwNjkxMjI@._V1_.jpg',
      Fantasy: 'https://m.media-amazon.com/images/M/MV5BNTU1MzgyMDMtMzBlZS00YzczLThmYWEtMjU3YmFlOWEyMjE1XkEyXkFqcGc@._V1_.jpg',
      Thriller: 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg',
      Animation: 'https://m.media-amazon.com/images/M/MV5BMTg5NzY0MzA2MV5BMl5BanBnXkFtZTYwNDc3NTc2._V1_FMjpg_UX1000_.jpg',
      Family: 'https://m.media-amazon.com/images/M/MV5BMjAwMzAzMzExOF5BMl5BanBnXkFtZTgwOTcwMDA5MTE@._V1_.jpg',
      War: 'https://m.media-amazon.com/images/M/MV5BMTkxNzI3ODI4Nl5BMl5BanBnXkFtZTgwMjkwMjY4MjE@._V1_FMjpg_UX1000_.jpg',
      Mystery: 'https://m.media-amazon.com/images/M/MV5BMTg0NjEwNjUxM15BMl5BanBnXkFtZTcwMzk0MjQ5Mg@@._V1_.jpg',
      Music: 'https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_.jpg',
      Musical: 'https://m.media-amazon.com/images/M/MV5BNTRlNmU1NzEtODNkNC00ZGM3LWFmNzQtMjBlMWRiYTcyMGRhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
      'Film-Noir': 'https://m.media-amazon.com/images/M/MV5BYmJiNTUwYWUtZDllNi00ODdjLWFmNTEtOTVlNmYxYTZhNzYzXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
      Sport: 'https://i.pinimg.com/736x/74/64/2e/74642e61235070450a84ddde496aa1f3.jpg'
    };

    genreSet.forEach(genre => {
      const tile = document.createElement("div");
      tile.className = "genre-tile";
      tile.innerHTML = `<span>${genre}</span>`;
      tile.onclick = () => {
        window.location.href = `genre.html?genre=${encodeURIComponent(genre)}`;
      };

      const imageUrl = genreImages[genre] || "https://via.placeholder.com/300x300?text=Genre";
      tile.style.setProperty('background-image', `url(${imageUrl})`);

      genreContainer.appendChild(tile);
    });
  }
});


hasShown = sessionStorage.getItem("hasShown");

function checkUserID() {
  userID = localStorage.getItem("userID");

  if (!userID) {
    userID = getUserID();
    localStorage.setItem('userID', userID);
    localStorage.setItem('likedMovies', null);
    sessionStorage.setItem('hasShown', false);
  }
  // else
  // {
  //   localStorage.clear();
  // }
  console.log(userID);
  document.getElementById("username-holder").textContent = userID;

  if (!hasShown) {
    const widget = document.getElementById("welcome-widget");
    widget.classList.add('welcome-visible');

    setTimeout(() => {
      widget.classList.remove("welcome-visible");
    }, 3000);
    sessionStorage.setItem("hasShown", true);
  }
}

function getUserID() {
  return 'guest_' + Math.random().toString(36).substr(2, 9);
}

checkUserID();
