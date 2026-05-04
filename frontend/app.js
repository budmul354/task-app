const API = "http://127.0.0.1:8000";
let token = null;

async function login() {
    const res = await fetch(`${API}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: "test@mail.com",
            password: "123456"
        })
    });

    const data = await res.json();
    token = data.access_token;
    loadTasks();
}

async function loadTasks() {
    const res = await fetch(`${API}/tasks`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await res.json();
    console.log(data);
}