# EduPortal - University Management System

Welcome to **EduPortal**, an Open Source University Management System built with **Flask** (Python) and **TailwindCSS**.

## 🚀 Getting Started

Follow this guide to set up the project locally from scratch.

### 1. Prerequisites
Ensure you have the following installed on your machine:
*   **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
*   **Node.js & npm** (for TailwindCSS): [Download Node.js](https://nodejs.org/)
*   **PostgreSQL**: [Download PostgreSQL](https://www.postgresql.org/download/)

### 2. Clone the Repository
```bash
git clone <repository-url>
cd EDU-PORTAL
```

### 3. Backend Setup (Python)
Create a virtual environment and install dependencies.

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Frontend Setup (TailwindCSS)
Install the Node.js dependencies required for compiling TailwindCSS.

```bash
npm install
```

### 5. Configuration & Database Setup

**A. Environment Variables**
1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    *(On Windows, just copy and rename `.env.example` to `.env`)*
2.  Open `.env` and update the database credentials (`DB_USER`, `DB_PASSWORD`, etc.) to match your local PostgreSQL setup.

**B. Create Database**
Open your PostgreSQL terminal (psql or pgAdmin) and create the database:
```sql
CREATE DATABASE "EduPortal";
```
*(Make sure the name matches `DB_NAME` in your `.env` file)*

**C. Initialize & Seed Database**
Run the management script to create tables and populate them with sample data (Students, Faculty, Courses, Attendance, etc.).

```bash
python manage.py seed
```
*This command drops existing tables, creates new ones, and fills them with optimized test data.*

### 6. Running the Application

You need two terminals running simultaneously:

**Terminal 1: TailwindCSS Compiler (Frontend)**
Watches for HTML changes and rebuilds CSS in real-time.
```bash
npm run dev
```

**Terminal 2: Flask Server (Backend)**
Runs the Python web server.
```bash
flask run
```

Access the application at: **http://127.0.0.1:5000**

---

## 📚 Documentation Index

We have divided the detailed documentation into specific modules:

### 🏗️ Architecture & Core
*   [**Project Functional Spec**](docs/PROJECT_FUNCTIONAL_SPEC.md) - User Personas, Journeys, and Vision.
*   [**System Architecture**](docs/ARCHITECTURE.md) - App Factory Pattern, Directory Structure.
*   [**Database Schema**](docs/DATABASE_SCHEMA.md) - ERD, Model Relationships.

### 🧠 Logic & Algorithms
*   [**Feature & Data Flow Deep Dive**](docs/FEATURES_AND_DATA_FLOW.md) - Enrollment, Attendance, Exams.
*   [**Admin Module Deep Dive**](docs/ADMIN_MODULE_DEEP_DIVE.md) - Prediction Algorithms, PDF Generation.
*   [**Reports Manual**](docs/REPORTS_MANUAL.md) - How to interpret AI Faculty Intelligence.

### 🛠️ Developer Resources
*   [**Contributing Guide**](CONTRIBUTING.md) - Code Style, PR Process.
*   [**Deployment Guide**](docs/DEPLOYMENT.md) - Production Setup (Gunicorn, Nginx).

---

## 🔑 Default Login Credentials (Seeded Data)

*   **Admin**: `admin@edu.com` / `123`
*   **Faculty**: `faculty1@edu.com` / `123`
*   **Student**: `student1@edu.com` / `123`