console.log("SCRIPT LOADED")

window.addEventListener("DOMContentLoaded", () => {

  const internshipGrid =
    document.getElementById("internshipGrid")

  const loader =
    document.getElementById("loader")

  const themeToggle =
    document.getElementById("themeToggle")

  const loadMoreBtn =
    document.getElementById("loadMoreBtn")

  const locationFilter =
  document.getElementById("locationFilter")

  const paidFilter =
    document.getElementById("paidFilter")


  // ---------------- GLOBAL DATA ----------------

  let allInternships = []

  let visibleInternships = []

  let visibleCount = 10

  let currentMode = "normal"


  // ---------------- THEME ----------------

  if (localStorage.getItem("theme") === "dark") {

    document.body.classList.add("dark-mode")

    if (themeToggle) {
      themeToggle.innerHTML = "☀️"
    }
  }

  if (themeToggle) {

    themeToggle.addEventListener("click", () => {

      document.body.classList.toggle("dark-mode")

      if (
        document.body.classList.contains("dark-mode")
      ) {

        themeToggle.innerHTML = "☀️"

        localStorage.setItem("theme", "dark")

      } else {

        themeToggle.innerHTML = "🌙"

        localStorage.setItem("theme", "light")
      }
    })
  }


  // ---------------- SEARCH ----------------

  window.searchInternships =
    async function(mode) {

      const query =
        document.getElementById("searchInput").value

      if (!query) {

        alert("Please enter a keyword.")

        return
      }

      loader.classList.remove("hidden")

      internshipGrid.innerHTML = ""

      if (loadMoreBtn) {
        loadMoreBtn.style.display = "none"
      }

      const buttons =
        document.querySelectorAll(
          ".search-buttons button"
        )

      buttons.forEach(btn => {
        btn.disabled = true
      })

      try {

        const response = await fetch(
          `http://127.0.0.1:5000/search?keyword=${query}&mode=${mode}`
        )

        const data =
          await response.json()

        console.log(
          "RESPONSE DATA:",
          data
        )

        if (!Array.isArray(data)) {

          console.error(
            "Invalid response:",
            data
          )

          alert(
            "Backend returned invalid data."
          )

          return
        }

        currentMode = mode

        allInternships = data

        visibleCount = 10

        if (mode === "pro") {

          visibleInternships =
            allInternships.slice(
              0,
              visibleCount
            )

        } else {

          visibleInternships =
            allInternships
        }

          applyFilters()

      } catch (error) {

        console.error(error)

        alert(
          "Failed to fetch internships."
        )

      } finally {

        buttons.forEach(btn => {
          btn.disabled = false
        })

        loader.classList.add("hidden")
      }
    }


  // ---------------- ENRICH ----------------

  window.getInternshipDetails =
    async function(link, button) {

      button.innerText = "Fetching..."

      button.disabled = true

      try {

        const response = await fetch(
          "http://127.0.0.1:5000/enrich-single",
          {
            method: "POST",

            headers: {
              "Content-Type": "application/json"
            },

            body: JSON.stringify({
              link
            })
          }
        )

        const data =
          await response.json()

        const internship =
          allInternships.find(
            job => job.Link === link
          )

        if (internship) {

          Object.assign(
            internship,
            data
          )

          updateSingleCard(
            internship
          )
        }

        button.innerText = "Enriched"

      } catch (error) {

        console.error(error)

        button.innerText = "Retry"

        button.disabled = false

        alert(
          "Failed to enrich internship."
        )
      }
    }

  // ---------------- FILTERS ----------------
  
  function applyFilters() {

  const selectedLocation =

    locationFilter.value.toLowerCase()

  const selectedPaid =

    paidFilter.value.toLowerCase()


  let filtered =
    [...allInternships]


  // ---------- LOCATION FILTER ----------

  if (selectedLocation) {

    filtered = filtered.filter(job =>

      job.Location &&
      job.Location
        .toLowerCase()
        .includes(selectedLocation)
    )
  }


  // ---------- PAID FILTER ----------

  if (selectedPaid === "paid") {

    filtered = filtered.filter(job =>

      job.Stipend &&
      !job.Stipend
        .toLowerCase()
        .includes("unpaid")
    )
  }

  if (selectedPaid === "unpaid") {

    filtered = filtered.filter(job =>

      job.Stipend &&
      job.Stipend
        .toLowerCase()
        .includes("unpaid")
    )
  }


  // ---------- PAGINATION ----------

  if (currentMode === "pro") {

    visibleInternships =
      filtered.slice(0, visibleCount)

  } else {

    visibleInternships = filtered
  }

  displayInternships()
}

  // ---------------- UPDATE CARD ----------------

  function updateSingleCard(updatedJob) {

    const cards =
      document.querySelectorAll(".card")

    cards.forEach(card => {

      const cardLink =
        card.getAttribute("data-link")

      if (cardLink === updatedJob.Link) {

        let skillsHTML = ""

        if (updatedJob.Skills) {

          skillsHTML =

            String(updatedJob.Skills)

              .split(",")

              .map(skill =>

                `<span class="skill">
                  ${skill.trim()}
                </span>`

              )

              .join("")
        }

        card.querySelector(
          ".skills-section"
        ).innerHTML =

          `
            <p class="skills-heading">

              Skills Required:

            </p>

            <div class="skills">

              ${skillsHTML}

            </div>
          `
        }
    } )
  }

  // ---------------- AutoEnrich ----------------
  async function autoEnrichVisibleCards() {

    const cards =
      document.querySelectorAll(".card")

    for (const card of cards) {

      const detailButton =
        card.querySelector(".detail-btn")

      if (
        detailButton &&
        detailButton.innerText === "Get Details" &&
        !card.dataset.enriched
      ){

        const link =
          card.getAttribute("data-link")

        await getInternshipDetails(
          link,
          detailButton
        )
        card.dataset.enriched = "true"
      }
    }
  }

  // ---------------- DISPLAY ----------------



  function displayInternships() {

    internshipGrid.innerHTML = ""

    if (
      !visibleInternships ||
      visibleInternships.length === 0
    ) {

      internshipGrid.innerHTML = `

        <div class="empty-state">

          No internships found.

        </div>

      `

      return
    }

    visibleInternships.forEach((job) => {
      console.log("Rendering job:", job)
      try {

        if (!job) {
          return
        }

        if (typeof job !== "object") {
          return
        }

        if (!job.Link) {
          return
        }

        const title =
          String(job.Title || "No Title")

        const company =
          String(
            job.Company ||
            "Unknown Company"
          )

        const location =
          String(
            job.Location || "Remote"
          )

        const stipend =

          job.Stipend
            ? String(job.Stipend)
            : "Not Disclosed"

        const duration =
          job.Duration
            ? String(job.Duration)
            : "N/A"

        const link =
          String(job.Link || "#")

        let skillsHTML = ""

        if (job.Skills) {

          skillsHTML =

            String(job.Skills)

              .split(",")

              .map(skill =>

                `<span class="skill">
                  ${skill.trim()}
                </span>`

              )

              .join("")
        }

        const card =
          document.createElement("div")

        card.className = "card"

        card.setAttribute(
          "data-link",
          link
        )

        card.innerHTML = `

          <h2>${title}</h2>

          <p class="company">
            ${company}
          </p>

          <div class="details">

            <p>• <strong>Location:</strong> ${location}</p>

            <p>• <strong>Stipend:</strong> ${stipend}</p>

            <p>• <strong>Duration:</strong> ${duration}</p>

          </div>

          <div class="skills-section">

            ${
              skillsHTML
                ? `<p class="skills-heading">
                    Skills Required:
                  </p>`
                : ""
            }

            <div class="skills">

              ${skillsHTML}

            </div>

          </div>

          <div class="card-buttons">

            <a
              href="${link}"
              target="_blank"
              class="view-btn"
            >

              Open Internship

            </a>

            <button
              type="button"
              class="detail-btn"
            >

              ${job.Skills
                ? "Enriched"
                : "Get Details"}

            </button>

          </div>

        `

        const detailButton =
          card.querySelector(
            ".detail-btn"
          )

        if (!job.Skills) {

          detailButton.addEventListener(
            "click",
            () => {

              getInternshipDetails(
                link,
                detailButton
              )
            }
          )

        } else {

          detailButton.disabled = true
        }

        internshipGrid.appendChild(card)

      } catch (error) {

        console.error(
          "Card rendering failed:",
          error,
          job
        )
      }

    })
    if (currentMode === "pro") {

      autoEnrichVisibleCards()
    }

    // ---------------- LOAD MORE ----------------

    if (!loadMoreBtn) {
      return
    }

    if (currentMode !== "pro") {

      loadMoreBtn.style.display =
        "none"

      return
    }

    if (
      visibleInternships.length <
      allInternships.length
    ) {

      loadMoreBtn.style.display =
        "inline-block"

      loadMoreBtn.innerText =
        "Load More"

      loadMoreBtn.disabled = false

    } else {

      loadMoreBtn.style.display =
        "inline-block"

      loadMoreBtn.innerText =
        "End of List"

      loadMoreBtn.disabled = true
    }
  }


  // ---------------- LOAD MORE ----------------

  if (loadMoreBtn) {

    loadMoreBtn.addEventListener(
      "click",
      () => {

        visibleCount += 10

        visibleInternships =
          allInternships.slice(
            0,
            visibleCount
          )

        displayInternships()
      }
    )
  }

  if (locationFilter) {

  locationFilter.addEventListener(
    "change",
    applyFilters
    )
  }

  if (paidFilter) {

    paidFilter.addEventListener(
      "change",
      applyFilters
    )
  }

})