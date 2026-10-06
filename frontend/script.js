const searchInput = document.getElementById("searchInput");
const rows = document.querySelectorAll("tbody tr");

searchInput.addEventListener("input", function () {
    const searchText = searchInput.value.toLowerCase();

    rows.forEach(function (row) {
        const patientName = row
            .querySelector("td")
            .textContent
            .toLowerCase();

        if (patientName.includes(searchText)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});