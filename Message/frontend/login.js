async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

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
            // Guardar token localmente (para el chat)
            localStorage.setItem("token", data.access_token);

            // Redirigir a Grupos PASANDO el token por URL 
            window.location.href = `http://localhost:5173/?token=${data.access_token}`;
        } else {
            document.getElementById("error").innerText = "Credenciales incorrectas";
        }

    } catch (err) {
        console.error(err);
    }
}
