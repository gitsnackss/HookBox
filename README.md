# HookBox – Webhook Inbox & Replay

HookBox is a self‑hosted service that captures incoming webhooks, stores them for inspection, and lets you replay any captured request to a target URL. Built with FastAPI, SQLite (or optional Postgres), and a lightweight Jinja2 + HTMX dashboard, it provides a polished yet minimal MVP for debugging third‑party integrations.

## Core Features

- **Capture**: Stable public URL (`/i/{project_key}`) to collect real payloads.
- **Inspect**: Paginated dashboard with full header/body inspection.
- **Replay**: Replay stored webhooks to localhost or other targets with original headers.
- **Organize**: Multiple projects with isolated API keys.
- **Secure**: Per‑project API keys, rate limiting, and SSRF protection.

## Quick‑Start (Local)

1. **Clone the repo**
   ```bash
   git clone https://github.com/gitsnackss/HookBox.git
   cd HookBox
   ```

2. **Setup Environment**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env to set ADMIN_API_KEY
   ```

3. **Initialize Database**
   ```bash
   python scripts/init_db.py
   # Copy the generated Admin API Key!
   ```

4. **Run Server**
   ```bash
   uvicorn app.main:app --reload
   ```
   Open http://localhost:8000 to view the dashboard.

## Docker

```bash
docker-compose up --build
```

## API Usage

**Create Project**
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer YOUR_ADMIN_KEY" \
  -d '{"name":"My Project"}'
```

**Ingest Webhook**
```bash
curl -X POST http://localhost:8000/i/{inbox_key} -d '{"hello":"world"}'
```

**Replay Webhook**
```bash
curl -X POST http://localhost:8000/api/v1/webhooks/{id}/replay \
  -H "Authorization: Bearer {project_api_key}" \
  -d '{"target_url":"http://localhost:3000/webhook"}'
```

## License

MIT
