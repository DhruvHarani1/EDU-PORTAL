# Deployment Guide

This guide explains how to take EduPortal from "Localhost" to "Production".

## 1. Environment Configuration

In production, **never** use `.env.example`. Create a robust `.env` file:

```ini
# Security
SECRET_KEY=Input_A_Very_Long_Random_String_Here_Use_Python_Secrets
FLASK_ENV=production
FLASK_DEBUG=0

# Database (PostgreSQL Recommended)
DATABASE_URL=postgresql://user:password@localhost:5432/eduportal_prod

# Mail Server (For Notices/Password Reset)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your_api_key
```

---

## 2. Server Architecture

We recommend **Gunicorn** behind **Nginx**.

### A. Install Gunicorn
```bash
pip install gunicorn
```

### B. Run the App
```bash
# 4 Workers is standard for a 2-Core VPS
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### C. Nginx Configuration (Reverse Proxy)
Create `/etc/nginx/sites-available/eduportal`:

```nginx
server {
    listen 80;
    server_name eduportal.youruniversity.edu;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Serve Static Files Directly (Performance)
    location /static {
        alias /var/www/eduportal/app/static;
    }
}
```

---

## 3. Database Migration in Production

**Never** run `reset_db.py` in production! It drops tables.
Instead, use Alembic migrations:

```bash
flask db migrate -m "Deploying v1.0"
flask db upgrade
```

---

## 4. Security Checklist
1.  **HTTPS**: Use Certbot (`sudo certbot --nginx`) to enable SSL.
2.  **Firewall**: Allow only ports 80, 443, and 22 (SSH). Block 8000.
3.  **Backup**: specific cron job to dump Postgres database daily.
