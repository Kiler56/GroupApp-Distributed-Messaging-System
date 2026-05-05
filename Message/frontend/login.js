async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const messageElement = document.getElementById("message");

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const res = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        const data = await res.json();

        if (res.ok) {
            localStorage.setItem("token", data.access_token);
            window.location.href = `http://localhost:5173/?token=${data.access_token}`;
        } else {
            messageElement.style.color = "red";
            messageElement.innerText = "Credenciales incorrectas";
        }

    } catch (err) {
        console.error(err);
        messageElement.style.color = "red";
        messageElement.innerText = "Error de conexión";
    }
}

async function register() {
    const username = document.getElementById("reg-username").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;
    const messageElement = document.getElementById("message");

    try {
        const res = await fetch("http://127.0.0.1:8000/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const data = await res.json();

        if (res.ok) {
            messageElement.style.color = "green";
            messageElement.innerText = "Usuario registrado exitosamente. Ahora puedes iniciar sesión.";
            toggleForms();
        } else {
            messageElement.style.color = "red";
            messageElement.innerText = data.detail || "Error en el registro";
        }
    } catch (err) {
        console.error(err);
        messageElement.style.color = "red";
        messageElement.innerText = "Error de conexión";
    }
}

function toggleForms() {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const messageElement = document.getElementById("message");

    messageElement.innerText = "";
    
    if (loginForm.style.display === "none") {
        loginForm.style.display = "block";
        registerForm.style.display = "none";
    } else {
        loginForm.style.display = "none";
        registerForm.style.display = "block";
    }
}
