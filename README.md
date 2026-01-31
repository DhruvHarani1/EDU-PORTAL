# EduPortal - Comprehensive Documentation

Welcome to the official developer documentation for **EduPortal**.
This project is an Open Source University Management System built with Flask & TailwindCSS.

## 📚 Documentation Index

We have divided the documentation into deep-dive modules for clarity.

### 🏗️ Architecture & Core
*   [**Project Functional Spec**](docs/PROJECT_FUNCTIONAL_SPEC.md)
    *   *Start Here: User Personas, End-to-End Journeys, and Product Vision.*
*   [**System Architecture**](docs/ARCHITECTURE.md)
    *   *Includes: App Factory Pattern, Directory Structure, Request Lifecycle.*
*   [**Database Schema**](docs/DATABASE_SCHEMA.md)
    *   *Includes: ERD, Model Relationships, Auth vs Data separation.*

### 🧠 Logic & Algorithms
*   [**Feature & Data Flow Deep Dive**](docs/FEATURES_AND_DATA_FLOW.md)
    *   *Includes: "Black Box" explanations of Enrollment, Attendance Aggregation, and Exam Hierarchy.*
*   [**Admin Module Deep Dive**](docs/ADMIN_MODULE_DEEP_DIVE.md)
    *   *Includes: Prediction Algorithms, Dashboard Aggregation Logic, PDF Generation Strategy.*
*   [**Reports Manual (User Guide)**](docs/REPORTS_MANUAL.md)
    *   *Includes: How to interpret the AI Faculty Intelligence and Radar Charts.*

### 🛠️ Developer Resources
*   [**Contributing Guide**](CONTRIBUTING.md)
    *   *Start here! Setup, Code Style, and PR Process.*
*   [**Deployment Guide**](docs/DEPLOYMENT.md)
    *   *Going to Prod: Gunicorn, Nginx, and Security Checklist.*
*   **Installation**: `pip install -r requirements.txt`
*   **Database Init**: `python scripts/reset_db.py`

---

## 🚀 Key Features "Under the Hood"

### 1. The "Future Sight" AI
The prediction engine in `reports_mgmt.py` uses statistical variance modeling to project student salaries based on grade trajectory. It doesn't just read data; it "simulates" a placement season.

### 2. Browser-Native PDF Engine
We assume modern browser capabilities. The reporting engine renders A4-sized HTML with `@media print` directives, delegating PDF rasterization to the browser for pixel-perfect Tailwind rendering.

### 3. Dynamic Attendance Tables
The attendance system uses SQL aggregation (`func.count`, `case`) to generate summary percentages on-the-fly, avoiding the need for a separate "stats" table that could go out of sync.