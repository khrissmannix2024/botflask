/* Muestra un mensaje cuando hay error en el registro de usuario */
document.addEventListener("DOMContentLoaded", function () {
    var flashMessage = document.getElementById("flashMessage");
    if (flashMessage && flashMessage.textContent.trim() !== "") {
        var toast = new bootstrap.Toast(flashMessage);
        toast.show();
    }
});
