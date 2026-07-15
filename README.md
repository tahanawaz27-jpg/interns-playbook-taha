# Task Manager API — Starter Codebase

A small API for tracking tasks assigned to users. Built with FastAPI, SQLAlchemy, and SQLite.

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000/docs** for interactive API docs, where you can try out every endpoint directly in the browser.

## What's here

- `POST /users` — create a user
- `GET /users/{user_id}` — fetch a user
- `POST /tasks` — create a task for a user
- `GET /tasks/{user_id}` — list a user's tasks
- `DELETE /tasks/{task_id}` — delete a task

The database is a local SQLite file (`todo.db`) that gets created automatically the first time you run the app. Delete it any time to start fresh.

## Your task this week

1. Read through `main.py` end to end until you understand how a request flows from route → database → response.
2. Try out every endpoint via `/docs` with a few different inputs — including ones you'd expect to fail.
3. Pick **one bug to fix** or **one small feature to add**, based on what you find while exploring. Some things worth poking at: what happens with unusual inputs, what happens when you fetch data across different users, and what operations are missing entirely compared to what you'd expect from a task manager.
4. Open a pull request (or share a diff) with your change, plus a short note explaining what you found and why you fixed it that way.

There's no single "correct" answer expected here — the point is to practice reading unfamiliar code critically and defending a change you made to it.
