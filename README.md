# WAEC Elective Math AI

Self-paced WAEC Further Mathematics learning platform with lessons, solved past questions, AI tutor, equation solver, timed exams, revision deck, syllabus mapping, and admin tools.

## Quick Start On A New Laptop

### Requirements
- Node.js 20 or newer
- Yarn 1 via Corepack
- Python 3.11+ recommended
- MongoDB running locally or a MongoDB Atlas URI

### 1. Clone
```powershell
git clone https://github.com/iodsai/waec-gpt.git
cd waec-gpt
```

### 2. Backend Setup
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item env.sample .env
```

Edit `backend\.env`:
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=waecgpt
JWT_SECRET=replace-with-a-long-random-secret
EMERGENT_LLM_KEY=your-emergent-or-gemini-key
ADMIN_EMAIL=yawusyawus.email@gmail.com
ADMIN_PASSWORD=admin123
```

Start backend:
```powershell
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

On first startup, the backend seeds topics, lessons, questions, demo users, and the custom admin user from `ADMIN_EMAIL` / `ADMIN_PASSWORD`.

### 3. Frontend Setup
Open a second terminal:
```powershell
cd frontend
corepack enable
corepack yarn install
Copy-Item env.sample .env.development.local
corepack yarn start
```

Open:
```text
http://localhost:3000
```

Admin login:
```text
Email: yawusyawus.email@gmail.com
Password: admin123
```

## Useful Routes
- `/syllabus` - official WAEC Further Mathematics syllabus map
- `/lessons` - course lessons
- `/past-questions` - solved WAEC-style questions
- `/tutor` - AI Math Tutor
- `/exams` - quick drills and mock exams
- `/admin` - admin question/import tools
- `/admin/lesson-audit` - lesson completeness audit

## Verification
Frontend production build:
```powershell
cd frontend
corepack yarn build
```

Backend syntax smoke check:
```powershell
python -m py_compile backend\server.py backend\syllabus_data.py backend\seed_data_v3_extra.py
```
