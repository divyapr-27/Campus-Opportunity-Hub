document.addEventListener("DOMContentLoaded", () => {
    const flashes = document.querySelectorAll(".flash");

    setTimeout(() => {
        flashes.forEach((flash) => {
            flash.style.transition = "opacity 0.4s ease";
            flash.style.opacity = "0";
        });
    }, 3500);
});
