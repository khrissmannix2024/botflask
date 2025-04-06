const socket = io();

// Evento para enviar mensajes por WebSocket
document.getElementById("send-message").addEventListener("click", function () {
    const input = document.getElementById("chat-input");
    const message = input.value.trim();
    const receiverId = document.getElementById("chat-username").dataset.userId; // Corregido el dataset

    if (message && receiverId) {
        socket.emit("send_message", { receiver_id: receiverId, message: message });
        input.value = ""; // Limpiar input
    }
});

// Permitir enviar con Enter
document.getElementById("chat-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        document.getElementById("send-message").click();
    }
});

// Escuchar mensajes entrantes
socket.on("receive_message", function (data) {
    console.log("📩 Mensaje recibido:", data);
    const chatMessages = document.getElementById("chat-messages");
    const mensajeElemento = document.createElement("div");
    mensajeElemento.textContent = data.message;
    mensajeElemento.classList.add("p-2", "rounded", "mb-2");

    if (parseInt(data.sender_id) === parseInt(usuarioActual)) { // Convertir a número para evitar errores
        mensajeElemento.classList.add("bg-primary", "text-white", "text-end");
    } else {
        mensajeElemento.classList.add("bg-light");
    }

    chatMessages.appendChild(mensajeElemento);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
});

// Función para mostrar los usuarios en el menú lateral
function mostrarUsuariosEnSidebar(usuarios) {
    const listaUsuarios = document.getElementById("lista-usuarios"); // Ahora usamos el sidebar
    if (!listaUsuarios) {
        console.error("El contenedor de usuarios no existe en el DOM.");
        return;
    }
    
    listaUsuarios.innerHTML = ""; // Limpiar la lista antes de agregar usuarios

    usuarios.forEach(usuario => {
        const usuarioItem = document.createElement("li");
        usuarioItem.textContent = usuario.username;
        usuarioItem.classList.add("list-group-item");
        usuarioItem.dataset.userId = usuario.id;
        
        // Agregar evento para abrir el modal al hacer clic en un usuario
        usuarioItem.addEventListener("click", function () {
            abrirModalChat(usuario.id, usuario.username);
        });

        listaUsuarios.appendChild(usuarioItem);
    });
}

// Obtener la lista de usuarios al cargar la página
document.addEventListener("DOMContentLoaded", function () {
    if (usuarioAutenticado === "true") {
        fetch("/api/usuarios")
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error al obtener usuarios");
                }
                return response.json();
            })
            .then(data => {
                console.log("Usuarios cargados:", data);
                mostrarUsuariosEnSidebar(data);
            })
            .catch(error => console.error("Error al obtener usuarios:", error));
    }
});

// Función para abrir el modal de chat
function abrirModalChat(id, username) {
    console.log("Abrir chat con", username);

    // Actualizar el título del modal
    document.getElementById("chat-username").textContent = username;
    document.getElementById("chat-username").dataset.userId = id;

    // Limpiar el área de mensajes
    const chatMessages = document.getElementById("chat-messages");
    chatMessages.innerHTML = "<p class='text-muted'>Cargando mensajes...</p>";

    // Hacer una petición para obtener los mensajes previos
    fetch(`/api/mensajes/${id}`)
        .then(response => response.json())
        .then(data => {
            chatMessages.innerHTML = ""; // Limpiar antes de agregar mensajes
            data.forEach(mensaje => {
                const mensajeElemento = document.createElement("div");
                mensajeElemento.textContent = mensaje.texto;
                mensajeElemento.classList.add("p-2", "rounded", "mb-2");
                
                // Si el mensaje es del usuario actual, alinearlo a la derecha
                if (parseInt(mensaje.remitente_id) === parseInt(usuarioActual)) {
                    mensajeElemento.classList.add("bg-primary", "text-white", "text-end");
                } else {
                    mensajeElemento.classList.add("bg-light");
                }
                
                chatMessages.appendChild(mensajeElemento);
            });
        })
        .catch(error => console.error("Error al obtener mensajes:", error));

    // Mostrar el modal de chat
    const chatModal = new bootstrap.Modal(document.getElementById("chatModal"));
    chatModal.show();
}