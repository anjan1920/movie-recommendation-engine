const API_BASE = "http://127.0.0.1:8000";


async function loadGenres() {
  try {
    const res = await fetch(`${API_BASE}/genres`);
    const genres = await res.json();

    const container = document.getElementById("genre-container");
    container.innerHTML = "";

    genres.forEach(item => {
      const tile = document.createElement("div");

      tile.className = `
        relative w-[220px] h-[220px]
        flex items-center justify-center
        rounded-xl cursor-pointer
        bg-center bg-cover
        text-white text-2xl font-bold
        overflow-hidden
        transition-transform duration-300
        hover:scale-105
      `;

      tile.style.backgroundImage = `url(${item.image || "https://via.placeholder.com/300"})`;

      tile.innerHTML = `
        <div class="absolute inset-0 bg-black/40 backdrop-blur-[1px]"></div>
        <span class="relative z-10">${item.genre}</span>
      `;

      tile.onclick = () => {
        //navigate to next page
        window.location.href = `genre.html?genre=${encodeURIComponent(item.genre)}`;
      };

      container.appendChild(tile);
    });
  } catch (err) {
    console.error("Failed to load genres:", err);
  }
}

/* ---------------- USER / SESSION ---------------- */

function initUser() {
  let userID = localStorage.getItem("userID");
  console.log("User ID",userID);
  

  if (!userID) {
    userID = "guest_" + Math.random().toString(36).slice(2, 9);
    localStorage.setItem("userID", userID);
    localStorage.setItem("likedMovies", JSON.stringify([]));
    sessionStorage.setItem("hasShown", "false");
  }

  document.getElementById("username-holder").textContent = userID;
  showWelcomeOnce();
}

function showWelcomeOnce() {
  if (sessionStorage.getItem("hasShown") === "true") return;

  const widget = document.getElementById("welcome-widget");
  widget.classList.remove("-top-24");
  widget.classList.add("top-8");

  setTimeout(() => {
    widget.classList.remove("top-8");
    widget.classList.add("-top-24");
  }, 3000);

  sessionStorage.setItem("hasShown", "true");
}


initUser();
loadGenres();
