const API = window.TASK_APP_API_URL || "http://127.0.0.1:8000";
const TOKEN_KEY = "task_app_token";
const EMAIL_KEY = "task_app_email";

let token = localStorage.getItem(TOKEN_KEY);
let currentEmail = localStorage.getItem(EMAIL_KEY);

const authPanel = document.getElementById("authPanel");
const taskPanel = document.getElementById("taskPanel");
const loginForm = document.getElementById("loginForm");
const taskForm = document.getElementById("taskForm");
const emailInput = document.getElementById("emailInput");
const passwordInput = document.getElementById("passwordInput");
const taskInput = document.getElementById("taskInput");
const taskList = document.getElementById("taskList");
const emptyState = document.getElementById("emptyState");
const statusMessage = document.getElementById("statusMessage");
const userLabel = document.getElementById("userLabel");
const loginButton = document.getElementById("loginButton");
const addButton = document.getElementById("addButton");
const logoutButton = document.getElementById("logoutButton");

if (currentEmail) {
    emailInput.value = currentEmail;
}

loginForm.addEventListener("submit", (event) => {
    event.preventDefault();
    login();
});

taskForm.addEventListener("submit", (event) => {
    event.preventDefault();
    addTask();
});

logoutButton.addEventListener("click", logout);

if (token) {
    showTaskPanel();
    loadTasks();
} else {
    showAuthPanel();
}

async function login() {
    const email = emailInput.value.trim();
    const password = passwordInput.value;

    setStatus("");
    setBusy(loginButton, true, "Signing in");

    try {
        const data = await request("/login", {
            method: "POST",
            body: {
                email,
                password
            }
        });

        token = data.access_token;
        currentEmail = email;
        localStorage.setItem(TOKEN_KEY, token);
        localStorage.setItem(EMAIL_KEY, email);
        passwordInput.value = "";

        showTaskPanel();
        await loadTasks();
    } catch (error) {
        setStatus(error.message || "Sign in failed.");
    } finally {
        setBusy(loginButton, false, "Sign in");
    }
}

async function loadTasks() {
    if (!token) {
        showAuthPanel();
        return;
    }

    setStatus("");

    try {
        const tasks = await request("/tasks", {
            auth: true
        });

        renderTasks(tasks);
    } catch (error) {
        if (error.status === 401) {
            logout("Session expired. Sign in again.");
            return;
        }

        setStatus(error.message || "Could not load tasks.");
    }
}

async function addTask() {
    const title = taskInput.value.trim();

    if (!title) {
        taskInput.focus();
        return;
    }

    setStatus("");
    setBusy(addButton, true, "Adding");

    try {
        const task = await request("/tasks", {
            method: "POST",
            auth: true,
            body: { title }
        });

        taskInput.value = "";
        prependTask(task);
        updateEmptyState();
        taskInput.focus();
    } catch (error) {
        if (error.status === 401) {
            logout("Session expired. Sign in again.");
            return;
        }

        setStatus(error.message || "Could not add task.");
    } finally {
        setBusy(addButton, false, "Add");
    }
}

async function request(path, options = {}) {
    const headers = {
        "Accept": "application/json"
    };

    if (options.body) {
        headers["Content-Type"] = "application/json";
    }

    if (options.auth) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API}${path}`, {
        method: options.method || "GET",
        headers,
        body: options.body ? JSON.stringify(options.body) : undefined
    });

    let data = null;
    const text = await response.text();

    if (text) {
        try {
            data = JSON.parse(text);
        } catch {
            data = text;
        }
    }

    if (!response.ok) {
        const error = new Error(getErrorMessage(data, response.status));
        error.status = response.status;
        throw error;
    }

    return data;
}

function getErrorMessage(data, status) {
    if (data && typeof data === "object" && data.detail) {
        return Array.isArray(data.detail) ? "Please check the entered values." : data.detail;
    }

    return `Request failed with status ${status}.`;
}

function renderTasks(tasks) {
    taskList.innerHTML = "";
    tasks.forEach(prependTask);
    updateEmptyState();
}

function prependTask(task) {
    const item = document.createElement("li");
    item.className = "task-item";

    const title = document.createElement("span");
    title.className = "task-title";
    title.textContent = task.title;

    const status = document.createElement("span");
    status.className = "task-status";
    status.textContent = task.status;

    item.append(title, status);
    taskList.prepend(item);
}

function updateEmptyState() {
    emptyState.hidden = taskList.children.length > 0;
}

function showTaskPanel() {
    authPanel.hidden = true;
    taskPanel.hidden = false;
    userLabel.textContent = currentEmail || "";
    taskInput.focus();
}

function showAuthPanel() {
    authPanel.hidden = false;
    taskPanel.hidden = true;
    emailInput.focus();
}

function logout(message = "") {
    token = null;
    localStorage.removeItem(TOKEN_KEY);
    showAuthPanel();
    taskList.innerHTML = "";
    setStatus(message);
}

function setBusy(button, isBusy, label) {
    button.disabled = isBusy;
    button.textContent = label;
}

function setStatus(message) {
    statusMessage.textContent = message;
}

window.addTask = addTask;
