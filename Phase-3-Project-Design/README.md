# Phase 3 – Project Design

## 1. System Architecture

PocketSmart AI follows a modular web application architecture.

The major layers are:

1. User Interface Layer
2. Application/API Layer
3. Service Layer
4. AI Integration Layer
5. Database Layer

### Architecture Flow

User
↓
Web Interface
↓
FastAPI Application
↓
Planner / Recommendation Services
↓
Gemini AI Integration
↓
Recommendation Result
↓
SQLite Database

## 2. User Interface Design

The application provides a web-based interface containing:

- Landing Page
- Registration Page
- Login Page
- Dashboard
- Home Interior Planner
- Party Planner
- Jewelry Planner
- Recommendation Results
- Recommendation History

The interface is designed to provide simple navigation and clear presentation of budget recommendations.

## 3. Application Design

FastAPI is used as the main backend framework.

The application is organized into modules:

### Authentication

Handles:

- User registration
- User login
- Session management

### Pages

Handles web page rendering using Jinja2 templates.

### Planners

Handles planner-related requests for:

- Home Interior
- Party
- Jewelry

### Services

The service layer contains:

- Catalog service
- Recommendation service

These services separate business logic from the application routes.

## 4. AI Integration Design

Google Gemini API is integrated into the application for AI-assisted recommendation generation.

The AI component contains:

- Gemini client
- Recommendation prompts
- Structured recommendation generation

User requirements and budget information are passed to the AI component, and the generated recommendation is processed and displayed to the user.

## 5. Database Design

SQLite is used as the application's database.

The database is used to store application data such as:

- User information
- Authentication-related data
- Generated recommendation plans
- Recommendation history

SQLAlchemy is used for database interaction.

## 6. Project Directory Design

```text
app/
├── ai/
│   ├── gemini_client.py
│   └── prompts.py
│
├── routers/
│   ├── auth.py
│   ├── pages.py
│   └── planners.py
│
├── services/
│   ├── catalog_service.py
│   └── recommendation_service.py
│
├── auth.py
├── config.py
├── database.py
├── main.py
├── models.py
└── schemas.py
Other major project components include:
data/
static/
templates/
tests/
uploads/
## 7. Data Flow

The basic recommendation flow is:

1. User logs into the application.
2. User selects a planner.
3. User enters budget and requirements.
4. FastAPI receives the request.
5. The recommendation service processes the request.
6. Gemini AI generates recommendations when available.
7. The generated plan is returned to the application.
8. The recommendation is displayed to the user.
9. The plan can be stored and accessed through history.

## 8. Security Design

The application follows basic security practices including:

- Password hashing
- Session-based authentication
- Environment variables for sensitive configuration
- API key protection using `.env`
- Input validation
- Ignoring sensitive files through `.gitignore`

## 9. Design Summary

The system design separates the user interface, backend routes, business services, AI integration and database components.

This modular design makes PocketSmart AI easier to develop, test, maintain and extend in future phases.