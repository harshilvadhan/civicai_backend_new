# CivicAI Backend

FastAPI + Supabase backend for the AI-powered Civic Complaint Routing System.

---

## 📁 Project Structure

```
backend/
├── main.py               ← FastAPI app entry point
├── config.py             ← Environment settings
├── models.py             ← Pydantic schemas
├── requirements.txt
├── Procfile              ← Railway start command
├── railway.toml          ← Railway config
├── schema.sql            ← Run this in Supabase SQL Editor
├── seed.py               ← Optional: seed demo data
├── routers/
│   ├── complaints.py     ← POST /complaints, GET /complaints/{ticket_id}
│   ├── officer.py        ← Officer login + queue + status update
│   └── upload.py         ← POST /upload/image
└── services/
    └── db_service.py     ← All Supabase queries
```

---

## 🚀 Setup (5 minutes)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Fill in your SUPABASE_URL and SUPABASE_KEY
```

### 3. Create database tables
- Open Supabase project → SQL Editor
- Paste and run contents of `schema.sql`
- Go to Storage → Create bucket named `complaint-images` → set to **Public**

### 4. Run locally
```bash
uvicorn main:app --reload
```

### 5. View Swagger docs
Open http://localhost:8000/docs

### 6. Seed sample data (optional)
```bash
python seed.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Who uses it |
|--------|----------|-------------|
| POST | `/complaints/` | Person 1 (Frontend) — submit confirmed complaint |
| GET | `/complaints/{ticket_id}` | Person 1 — citizen tracking |
| POST | `/upload/image` | Person 1 — upload photo, get URL back |
| POST | `/officer/login` | Person 4 (Dashboard) — officer login |
| GET | `/officer/complaints` | Person 4 — load complaint queue |
| PATCH | `/officer/complaints/{id}/status` | Person 4 — update status |

---

## 🔗 Integration with Person 3 (AI Engine)

**Flow:**
1. Person 1 sends `{user_text, image_base64}` to Person 3's AI
2. AI returns `{category, urgency, formal_complaint, suggested_department, reasoning}`
3. Person 1 shows citizen a review screen
4. Citizen confirms → Person 1 sends everything to `POST /complaints/`
5. We save it. No AI parsing needed on our side.

---

## 🔐 Officer Auth (Hackathon)
- Email: `officer@civicai.in`
- Password: `demo1234`
- Token: `Authorization: Bearer officer-secret-token`

---

## 🚂 Deploy to Railway

1. Push this folder to a GitHub repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SUPABASE_BUCKET` = `complaint-images`
4. Railway auto-deploys and gives you a live URL

Your backend URL will be: `https://<your-app-name>.up.railway.app`
Swagger docs: `https://<your-app-name>.up.railway.app/docs`
