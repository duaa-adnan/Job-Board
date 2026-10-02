# Job Board

A small job board I built as a take-home project. Recruiters can post jobs, candidates can apply to them, and the recruiter can move each candidate through hiring stages. It's a CRUD app with a Python backend, a SQLite database and a simple web page.

## Live demo

https://job-board-11131.containers.snapdeploy.app/board

This runs on a free hosting plan. If nobody has opened it for a while, the first load can take up to a minute while it wakes up. The demo data also resets whenever the app restarts, because the free plan doesn't keep the SQLite file.

## What it does

- Create, view, edit and delete jobs
- Candidates can apply to a job with a name and email
- Closed jobs don't accept applications
- The same email can't apply to the same job twice (the database enforces this)
- Candidates move through stages: applied, interviewing, hired, rejected
- Deleting a job also deletes its candidates
- There's a JSON API (docs at `/docs`) and a simple web page at `/board`

## Tech stack

- **FastAPI** for the backend. It's quick to set up, validates input for me, and generates API docs automatically.
- **SQLite with SQLAlchemy** for the database. There's nothing to install and it's enough for a project this size.
- **Jinja2 templates and plain CSS** for the frontend, so there's no separate build step.

## How to run it

You need Python 3.10 or newer.

```
git clone https://github.com/duaa-adnan/Job-Board.git
cd Job-Board
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

On Mac or Linux, use `python3 -m venv venv` and `source venv/bin/activate` instead.

Then open:

- http://127.0.0.1:8000/board for the web page
- http://127.0.0.1:8000/docs for the API docs

The database file (`jobs.db`) is created automatically the first time the app starts.

## API endpoints

| Method | Path | What it does |
|---|---|---|
| GET | `/health` | Checks the app is running |
| POST | `/jobs` | Create a job |
| GET | `/jobs` | List all jobs |
| GET | `/jobs/{id}` | Get one job |
| PUT | `/jobs/{id}` | Update a job |
| DELETE | `/jobs/{id}` | Delete a job |

Candidates are handled through the web page (`/board`) and don't have a JSON API yet.

## What I would add next

- A JSON API for candidates, like the one for jobs
- Login, so only recruiters can edit jobs and move candidates
- Validation on the web forms that matches the API rules
- Automated tests
- A move to PostgreSQL if it ever needed real traffic