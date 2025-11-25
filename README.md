# Project_1internship_onssa
Stock Manager Pro is a web-based inventory system built with Flask and HTML/CSS/vanilla JS. It streamlines product tracking, delivery management, and employee control, offering real-time analytics, automatic ID generation, multi-format exports, and a secure, scalable architecture.
## 🎥 Project Demo Video
https://drive.google.com/file/d/1qWKB2iVnhDoj8i4UTLiqPhlPdo7NVuue/view?usp=drive_link

✔️ Version 1 — Frontend Only (HTML + CSS + JS + LocalStorage)

This version works 100% in the browser.
It uses LocalStorage, meaning:
No backend
No server
Data saved only on the user’s device
Fast + simple

Good for demos, small use cases, or offline mode
Limitations:
Data is not shared between devices
LocalStorage max ~5–10MB
No real security
Not scalable

✔️ Version 2 — Fullstack (Flask Backend + Frontend)

This version uses:
Flask API (Python) → database logic
PostgreSQL or SQLite → persistent storage
HTML/CSS/JS for the frontend
JWT / Flask-Login for authentication
Real security, real database, scalable

Advantages:
Can handle many users
Data stored on a server
Real authentication system
Real-time updates

Exports, charts, employees, deliveries… everything managed through the backend
