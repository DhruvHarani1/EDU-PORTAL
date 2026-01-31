# Contributing to EduPortal

Thank you for your interest in contributing! This project is Open Source and maintained by the community.
Please follow these guidelines to ensure a smooth collaboration.

## 🛠️ Development Setup

### 1. Project Initialization
We use **Python 3.9+** and **Node.js 16+**.

```bash
# Clone the repository
git clone https://github.com/your-org/EduPortal.git
cd EDU-PORTAL

# Create Virtual Environment (Essential)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Backend Deps
pip install -r requirements.txt
```

### 2. Database & Seeds
We use `scripts/` to manage the database state.
```bash
# Initialize DB Schema
flask db upgrade

# Reset & Seed Data (Admin: admin@edu.com / password)
python scripts/reset_db.py
```

### 3. Frontend Build (Tailwind)
We use a watcher to compile TailwindCSS on-the-fly.
```bash
npm install
npm run dev
```

---

## 📐 Coding Standards

### Python (Backend)
*   **Style**: Follow PEP 8.
*   **Blueprints**: All new features must be in their own blueprint (e.g., `app/library`).
*   **Models**: Use `db.ForeignKey` explicitly. Do not assume IDs.
*   **Imports**: Absolute imports only (`from app.models import User`, not `from ..models import User`).

### HTML/CSS (Frontend)
*   **Tailwind First**: Do not write custom CSS in `style` tags unless for print layouts.
*   **Jinja components**: Use `{% include %}` for reusable widgets (like headers/footers).

---

## 🔀 Pull Request Process

1.  **Fork** the repo and create your branch from `main`.
2.  **Test** your changes. ensure `python scripts/reset_db.py` still runs without error.
3.  **Update Documentation**: If you added a feature, update `FEATURES_AND_DATA_FLOW.md`.
4.  **Submit PR**: detailed description of "Why" and "How".

---

## 🧪 Testing
Currently, we rely on manual verification.
*   **Smoke Test**: Login as Admin, Click "Generate Report". If it generates PDF, core is working.
