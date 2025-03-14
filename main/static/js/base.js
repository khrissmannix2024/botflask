document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    const darkModeQuery = window.matchMedia("(prefers-color-scheme: dark)");

    function applyDarkModePreference() {
        if (darkModeQuery.matches) {
            body.setAttribute("data-bs-theme", "dark"); // Activa el modo oscuro
        } else {
            body.setAttribute("data-bs-theme", "light"); // Activa el modo claro
        }
    }
    applyDarkModePreference();
    darkModeQuery.addEventListener("change", applyDarkModePreference);
});