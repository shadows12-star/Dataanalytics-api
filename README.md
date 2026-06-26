# 📊 FastAPI Analytics — TimescaleDB Event Tracker

A lightweight, self-hosted web analytics backend built with **FastAPI**, **SQLModel**, and **TimescaleDB**. Track page views, session durations, operating systems, and referrers — all stored in a time-series database optimized for fast aggregation queries.

---

## ✨ Features

- 📈 **Time-bucketed analytics** — aggregate events by any time interval (e.g. `1 hour`, `1 day`, `1 week`)
- 🖥️ **OS detection** — automatically classifies user agents into Windows, Macintosh, Linux, iPhone, Android, or Other
- 🔗 **Referrer & session tracking** — understand where users come from and how long they stay
- 🗑️ **Automatic data retention** — data older than 3 months is automatically dropped via TimescaleDB policies
- 🐳 **Docker ready** — includes `Dockerfile`, `compose.yaml`, and Railway deployment config
- ⚡ **Built on TimescaleDB** — hypertable chunking for performant time-series storage and querying

---

## 🗂️ Project Structure

```
.
├── boot/
│   └── docker-run.sh          # Docker entrypoint script
├── nbs/
│   ├── hello-world.ipynb      # Quickstart notebook
│   └── verify-api-e....ipynb  # API verification notebook
├── src/
│   └── api/
│       ├── db/
│       │   ├── config.py      # Database configuration
│       │   └── session.py     # SQLModel session & engine setup
│       └── events/
│           ├── models.py      # EventModel, schemas, utilities
│           ├── routing.py     # API route handlers
│           └── __init__.py
│   └── main.py                # FastAPI app entry point
├── .env                       # Environment variables (gitignored)
├── .env.config                # Environment variable template
├── compose.yaml               # Docker Compose configuration
├── Dockerfile
├── railway.json               # Railway deployment config
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- A running TimescaleDB instance (or use the provided Compose setup)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Configure environment variables

```bash
cp .env.config .env
# Edit .env with your database credentials
```

Your `.env` should include:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/analytics
```

### 3. Run with Docker Compose

```bash
docker compose up --build
```

This starts both the FastAPI app and a TimescaleDB-enabled PostgreSQL instance.

### 4. Run locally (without Docker)

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

---

## 📡 API Reference

### `GET /api/events/`

Returns time-bucketed event aggregates grouped by page, OS, and time interval.

**Query Parameters:**

| Parameter  | Type     | Default   | Description                                      |
|------------|----------|-----------|--------------------------------------------------|
| `duration` | `string` | `"1 day"` | TimescaleDB time bucket interval (e.g. `1 hour`) |
| `pages`    | `list`   | See below | List of pages to filter (repeatable query param) |

**Default pages tracked:**
`/`, `/about`, `/pricing`, `/contact`, `/blog`, `/products`, `/login`, `/signup`, `/dashboard`, `/settings`

**Example Request:**

```bash
curl "http://localhost:8000/api/events/?duration=1%20hour&pages=/&pages=/pricing"
```

**Example Response:**

```json
[
  {
    "bucket": "2024-01-15T10:00:00Z",
    "page": "/pricing",
    "operating_system": "Macintosh",
    "avg_duration": 142.5,
    "count": 38
  }
]
```

---

### `POST /api/events/`

Records a new page view event.

**Request Body:**

```json
{
  "page": "/pricing",
  "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
  "ip_address": "192.168.1.1",
  "referrer": "https://google.com",
  "session_id": "abc123",
  "duration": 95
}
```

**Response:** The created `EventModel` object.

---

### `GET /api/events/{event_id}`

Retrieves a single event by its ID.

**Response:** `EventModel` or `404` if not found.

---

## 🗃️ Data Models

### `EventModel` (TimescaleDB Hypertable)

| Field        | Type            | Description                         |
|--------------|-----------------|-------------------------------------|
| `id`         | `int` (auto)    | Primary key                         |
| `time`       | `datetime`      | Event timestamp (partition key)     |
| `page`       | `str`           | Page path (e.g. `/about`)           |
| `user_agent` | `str` (optional)| Raw browser user agent string       |
| `ip_address` | `str` (optional)| Client IP address                   |
| `referrer`   | `str` (optional)| Referring URL                       |
| `session_id` | `str` (optional)| Client-generated session identifier |
| `duration`   | `int` (optional)| Time spent on page in seconds       |

**TimescaleDB settings:**
- Chunk interval: `1 day`
- Data retention: `3 months` (auto-dropped)

---

## 🐳 Deployment

### Railway

This project includes a `railway.json` for one-click Railway deployment. Connect your Railway project to this repo and set the required environment variables in the Railway dashboard.

### Docker

```bash
docker build -t fastapi-analytics .
docker run -p 8000:8000 --env-file .env fastapi-analytics
```

---

## 🛠️ Tech Stack

| Layer      | Technology                                                 |
|------------|------------------------------------------------------------|
| Framework  | [FastAPI](https://fastapi.tiangolo.com/)                   |
| ORM        | [SQLModel](https://sqlmodel.tiangolo.com/)                 |
| Database   | [TimescaleDB](https://www.timescale.com/) (PostgreSQL)     |
| Deployment | Docker, [Railway](https://railway.app/)                    |

---

## 📄 License

MIT — feel free to use this as a starting point for your own analytics stack.
