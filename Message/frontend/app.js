const API_MSG = "http://127.0.0.1:8001";
const API_AUTH = "http://127.0.0.1:8000";

// PEGA TU TOKEN AQUÍ
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJzdWIiOiJhcnR1cm9AZ21haWwuY29tIiwiZXhwIjoxNzc2NjY1MjM0fQ.1jgTNNWoz2CNCeAGIthx4VNvopui4x4c5kG6tYihSPc";

let currentUser = null;
let currentChat = null;


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
        const res = await fetch(`${API_AUTH}/groups`, {
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

    } catch (err) {
        console.error("Error cargando grupos:", err);
    }
}


document.getElementById("groupSelect").addEventListener("change", function () {
    currentChat = this.value;
    console.log("Chat seleccionado:", currentChat);
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

            if (msg.sender_id == currentUser.user_id) {
                div.textContent = "🟢 Yo: " + msg.content;
            } else {
                div.textContent = "🔵 " + msg.sender_id + ": " + msg.content;
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
            console.error("Error backend:", data);
            alert("Error al enviar mensaje");
            return;
        }

        input.value = "";
        loadMessages();

    } catch (err) {
        console.error("Error:", err);
    }
}


async function init() {
    await loadUser();
    await loadGroups();
}

init();

setInterval(loadMessages, 2000);