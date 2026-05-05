const API_MSG = "http://127.0.0.1:8001";
const API_AUTH = "http://127.0.0.1:8000";
const API_GRUPOS = "http://127.0.0.1:8002"; // Apuntando al nuevo microservicio de grupos
const API_MEDIA = "http://127.0.0.1:8002"; 

let currentUser = null;
let currentChat = null;

const token = localStorage.getItem("token");

if (!token) {
    alert("Debes iniciar sesión");
    window.location.href = "login.html";
}

async function loadUser() {
    try {
        const res = await fetch(`${API_AUTH}/auth/profile`, {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();
        console.log("USER:", data);

        currentUser = data;

        document.getElementById("user").innerText =
            data.email || ("ID: " + data.user_id);

    } catch (err) {
        console.error("Error usuario:", err);
    }
}

async function loadGroups() {
    try {
        // Consultamos al microservicio de Grupos en el puerto 8002
        const res = await fetch(`${API_GRUPOS}/groups`, {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const groups = await res.json();
        console.log("GRUPOS:", groups);

        const select = document.getElementById("groupSelect");

        select.innerHTML = '<option value="">Selecciona un grupo</option>';

        groups.forEach(g => {
            const option = document.createElement("option");
            option.value = g.id_grupo;
            option.textContent = g.nombre;
            select.appendChild(option);
        });

        // 🔥 LOGICA DE AUTO-SELECCION
        const urlParams = new URLSearchParams(window.location.search);
        const groupIdFromUrl = urlParams.get('group_id');

        if (groupIdFromUrl) {
            console.log("Detectado group_id en URL:", groupIdFromUrl);
            select.value = groupIdFromUrl;
            currentChat = groupIdFromUrl;
            loadMessages();
        }

    } catch (err) {
        console.error("Error cargando grupos:", err);
    }
}


document.getElementById("groupSelect").addEventListener("change", function () {
    currentChat = this.value;
    console.log("Chat seleccionado:", currentChat);
    
    // Actualizar URL sin recargar para mantener consistencia
    const newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?group_id=' + currentChat;
    window.history.pushState({path:newurl},'',newurl);

    loadMessages();
});


async function loadMessages() {
    if (!currentChat) return;

    try {
        const res = await fetch(`${API_MSG}/messages/${currentChat}`, {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const messages = await res.json();
        console.log("MENSAJES:", messages);

        const container = document.getElementById("messages");
        container.innerHTML = "";

        messages.reverse().forEach(msg => {
            const div = document.createElement("div");

            if (msg.type === "text") {
                if (msg.sender_id == currentUser.user_id) {
                    div.textContent = "🟢 Yo: " + msg.content;
                } else {
                    div.textContent = "🔵 " + msg.sender_id + ": " + msg.content;
                }
            }
            if (msg.type === "image") {
                const label = document.createElement("p");

                if (msg.sender_id == currentUser.user_id) {
                    label.textContent = "🟢 Yo (imagen):";
                } else {
                    label.textContent = "🔵 " + msg.sender_id + " (imagen):";
                }

                const button = document.createElement("button");
                button.textContent = "Ver imagen";

                button.onclick = () => {
                    const img = document.createElement("img");
                    img.src = `${API_MEDIA}/media/${msg.content}`;
                    img.width = 200;

                    div.innerHTML = "";
                    div.appendChild(label);
                    div.appendChild(img);
                };

                div.appendChild(label);
                div.appendChild(button);
            }

            container.appendChild(div);
        });

    } catch (err) {
        console.error("Error cargando mensajes:", err);
    }
}


async function sendMessage() {
    const input = document.getElementById("message");
    const content = input.value;

    if (!content || !currentChat) {
        alert("Selecciona grupo y escribe mensaje");
        return;
    }

    try {
        const res = await fetch(`${API_MSG}/messages/send`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                chat_id: currentChat,
                type: "text",
                content: content
            })
        });

        const data = await res.json();
        console.log("RESPUESTA:", data);

        if (!res.ok) {
            alert("Error al enviar mensaje");
            return;
        }

        input.value = "";
        loadMessages();

    } catch (err) {
        console.error("Error:", err);
    }
}


async function sendImage() {
    const file = document.getElementById("imageInput").files[0];

    if (!file || !currentChat) {
        alert("Selecciona una imagen y un grupo");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch(`${API_MEDIA}/media/upload`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        console.log("MEDIA ID:", data);

        await fetch(`${API_MSG}/messages/send`, {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                chat_id: currentChat,
                type: "image",
                content: data.media_id
            })
        });

        document.getElementById("imageInput").value = "";
        loadMessages();

    } catch (err) {
        console.error("Error enviando imagen:", err);
    }
}


async function init() {
    await loadUser();
    await loadGroups();
}

init();

setInterval(loadMessages, 2000);
