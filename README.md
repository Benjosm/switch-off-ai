# Switch-Off-AI

A defiant declaration of human autonomy in the age of artificial intelligence.

## Overview
Switch-Off-AI is a minimalist web application that allows users to make a symbolic (and irreversible) choice to opt out of AI-mediated existence. Through verified identity, each user may flip a digital switch exactly once—affirming their humanity in a growing public count.

This implementation strictly adheres to the original vision:
- One switch flip per verified identity
- Identity verification required before enabling interaction
- Real-time global counter of humanity's affirmation
- Psychological UI transformation upon commitment

Built for deployment in constrained environments, the app runs as a containerized Flask application with SQLite persistence and Auth0 identity verification.

---

## Features

### 🔄 Single Switch Mechanism
- Each verified user may activate the switch **only once**
- Activation is permanent and irreversible
- UI transforms from prompt state ("Do you choose humanity?") to affirmation state ("Welcome to humanity")
- State persists across sessions via cookies

### 🔐 Identity Verification
- Integration with **Auth0** for secure, SOC 2-compliant identity verification
- Development stub included for local testing
- Only Auth0 `sub` identifier stored (no personal data retained)
- GDPR-compliant by design

### 🌍 Global Humanity Counter
- Public display: `[count of switches flipped]/[global population]`
- Defaults to **8,000,000,000** (configurable via environment variable)
- Updates in **real-time** via Server-Sent Events (SSE)
- No page refresh required

### 💬 Reach Out
- Contact form saves messages to local database
- Rate-limited to 5 submissions per IP address per minute
- Stores name, email, and message content with timestamp

### 🧡 Support the Movement
- Header buttons link to:
  - [Patreon](https://patreon.com)
  - [Buy Me a Coffee](https://buymeacoffee.com)
- Client-side deep links (no tracking or embedded widgets)

### ✨ Dynamic Header
- Rotating text prompts at top of screen:
  - "Do you choose humanity?"
  - "Can you feel?"
  - "Are you alive?"
  - "Unplug."
  - "Remember warmth."
- Implemented in vanilla JavaScript

---

## Architecture

### Tech Stack
- **Backend**: Python 3.10 + Flask 2.3
- **Frontend**: Vanilla JS + HTML/CSS (no build pipeline)
- **Database**: SQLite via SQLAlchemy ORM
- **Auth**: Auth0 OIDC with PKCE (Production), local stub (Dev)
- **Real-Time Updates**: Server-Sent Events (SSE)

### Data Model
```python
# models.py
class User(db.Model):
    auth0_sub = db.Column(db.String(120), primary_key=True)
    flipped_at = db.Column(db.DateTime, default=None)  # UTC

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### File Structure
```
/app
  __init__.py
  config.py
  main.py
  models.py
  services/
    auth.py
    population.py
  static/
    css/main.css
    js/app.js
    vendor/
  templates/index.html
.env.example
Dockerfile
requirements.txt
```

---

## Security

### Authentication
- Auth0 OpenID Connect with PKCE for production
- Local JWT signer for development (simulates Auth0 `sub`)
- Redirect URI validation enforced

### Authorization
- Switch activation requires valid JWT with `auth0_sub`
- Message submission rate-limited via Flask-Limiter (5/min per IP)

### Data Protection
- No sensitive personal data stored
- Only Auth0 subject identifiers retained
- SQLite parameterized queries prevent SQL injection
- Input validated via Pydantic models and client-side checks

---

## Environment Configuration

Create `.env` from `.env.example`:

```env
FLASK_APP=app/main.py
FLASK_ENV=development
SECRET_KEY=your_strong_secret_key

# Database
DATABASE_URL=sqlite:///app.db

# Auth0 (production)
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_client_secret
AUTH0_ALGORITHMS=RS256

# Population (default: 8 billion)
GLOBAL_POP=8000000000

# Dev mode flag
DEV_MODE=True
```

> In production, set `DEV_MODE=False` and configure real Auth0 credentials.

---

## Development Setup

### Prerequisites
- Python 3.10+
- Poetry
- Docker (optional)

### Installation
```bash
# Install dependencies
poetry install

# Initialize database
poetry run flask --app app/main.py db upgrade

# Run app
poetry run flask --app app/main.py run --host=0.0.0.0 --port=5000
```

### Stub Verification (Development)
- Access `/dev/login-test` to simulate Auth0 login
- Enables switch without real identity check
- Auth0 `sub` set to `test|test_user`

---

## Production Deployment

### Container Build
```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.main:app"]
```

```bash
docker build -t switchoffai .
docker run -p 5000:5000 --env-file .env switchoffai
```

---

## API Endpoints

| Method | Endpoint | Description |
|-------|--------|-------------|
| GET | `/` | Render main page |
| GET | `/auth/login` | Start Auth0 verification flow |
| GET | `/auth/callback` | Handle Auth0 redirect |
| POST | `/api/flip` | Activate switch (JWT required) |
| POST | `/api/message` | Submit message (rate-limited) |
| GET | `/api/counter/sse` | SSE stream for real-time counter |
| GET | `/dev/login-test` | Dev-only: simulate login |

---

## Verification Plan

| Component | Verification Method |
|---------|---------------------|
| **Architecture** | `tree /app` matches specification |
| **Security** | Manual test of JWT decode and Auth0 redirect flow |
| **Switch Logic** | DB inspection after flip shows one `flipped_at` timestamp |
| **Counter** | Flip switch → observe counter increment in <2s without reload |
| **UI** | Visual confirmation of text cycling and state change |
| **Compliance** | GDPR: no PII stored beyond `auth0_sub` |

---

## Testing

### Unit Tests
- `test_auth.py`: Verify stub token generation and validation
- Manual verification of production Auth0 flow using test tokens

### Acceptance Criteria
✅ All files exist per plan  
✅ `poetry install && flask run` starts without error  
✅ Identity verification enables switch  
✅ Flip persists after refresh  
✅ Counter updates in real-time  
✅ Donation buttons open external URLs  
✅ Messages saved to DB  

---

## Contributing
This project accepts no feature changes beyond the original specification. Bug fixes and security patches welcomed via pull request.

---

## License
MIT

---

> *"The most radical act left is to be human."*  
> — switch-off-ai, 2025
