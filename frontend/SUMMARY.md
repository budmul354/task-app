# Frontend Summary

This folder contains the static browser frontend for Task App. It is a small single-page interface built with plain HTML, CSS, and JavaScript.

## What It Does

- Shows a login form for the backend user account.
- Sends JSON credentials to `POST /login`.
- Stores the returned bearer token in `localStorage`.
- Loads authenticated tasks from `GET /tasks`.
- Adds new tasks through `POST /tasks`.
- Shows task titles and statuses in a responsive list.
- Lets the user sign out by clearing the saved token.

## Key Files

- `index.html` defines the login panel, task panel, forms, task list, and status message area.
- `app.js` handles login, logout, task loading, task creation, API requests, local storage, and DOM updates.
- `style.css` provides the responsive layout, form styling, task list styling, buttons, and status states.

## User Flow

1. The user opens `index.html` in a browser.
2. If a token exists in `localStorage`, the app shows the task panel and attempts to load tasks.
3. Without a token, the app shows the login panel.
4. After successful login, the app saves the token and email, then loads tasks.
5. New tasks are submitted from the task form and inserted into the visible list.
6. If an authenticated request returns `401`, the app signs the user out and asks them to sign in again.

## Backend Connection

The frontend uses this API base URL by default:

```text
http://127.0.0.1:8000
```

To point the frontend at another backend, define `window.TASK_APP_API_URL` before `app.js` loads.

Example:

```html
<script>
  window.TASK_APP_API_URL = "https://api.example.com";
</script>
<script src="app.js" defer></script>
```

## Browser State

The app stores two values in `localStorage`:

- `task_app_token`: bearer token returned by the backend.
- `task_app_email`: last signed-in email, used to refill the login field and label the task view.

## UI Notes

The interface is intentionally minimal: a centered panel, accessible form fields, clear loading labels, an empty task state, and a mobile-friendly layout. It does not use a build step or external frontend framework.
