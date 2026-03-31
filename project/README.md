# AI-Assisted Skin Disease Diagnosis and Treatment Guidance System

## Tech Stack
- Python 3.9+
- Flask + Flask-SQLAlchemy + Flask-Login + Flask-Migrate + Flask-WTF
- OpenCV + NumPy + TensorFlow
- MySQL
- Bootstrap 5 + Jinja2

## Quick Start
```bash
cd project
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configure MySQL
1. Create MySQL database using `schema.sql`
2. Seed sample records using `seed_data.sql`
3. Optionally set env vars:
```bash
export DATABASE_URL='mysql+pymysql://root:password@localhost:3306/skin_diagnosis_db'
export SECRET_KEY='change-me'
```

### Run
```bash
python app.py
```
Open http://127.0.0.1:5000

## Features
- Multi-role authentication (User/Admin/Medical Expert)
- Image upload + OpenCV preprocessing + CNN inference
- Sample images can be added manually in `static/uploads/` (not bundled as binaries)
- Symptom-based classification fallback
- Disease/remedy retrieval and confidence display
- Chatbot backed by DB knowledge table
- Admin management dashboard and expert update panel
