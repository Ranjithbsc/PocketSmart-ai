# Phase 5 – Project Development

## 1. Development Overview

PocketSmart AI was developed as a modular web application using Python and FastAPI.

The application combines user authentication, budget planning, recommendation services, AI integration and recommendation history into a single platform.

## 2. Backend Development

The backend was developed using FastAPI.

The main backend components include:

- Application configuration
- Database connection
- Database models
- Request and response schemas
- Authentication
- Page routing
- Planner APIs
- Recommendation services

The backend handles user requests, validates input and connects the different application modules.

## 3. Authentication Development

The authentication module provides:

- User registration
- User login
- Session-based authentication
- Password protection
- Access control for authenticated pages

Users can create an account and securely access their planning dashboard.

## 4. Planner Development

Three main planners were developed:

### Home Interior Planner

The Home Interior Planner helps users plan requirements such as:

- Furniture
- Lighting
- Fans
- Dining requirements

### Party Planner

The Party Planner supports planning requirements related to:

- Venue
- Food
- Decoration
- Entertainment

### Jewelry Planner

The Jewelry Planner provides recommendations based on:

- Occasion
- Outfit
- Jewelry preferences
- Available budget

## 5. Recommendation Development

The recommendation system processes the user's:

- Budget
- Requirements
- Preferences
- Selected planner category

The system generates a recommendation plan and provides a budget breakdown.

A catalog service is also used to provide product and planning information.

## 6. AI Integration

Google Gemini API was integrated to provide AI-assisted recommendations.

The AI module contains:

- Gemini API client
- Recommendation prompts
- Structured recommendation generation

The application sends relevant planning information to the AI service and processes the generated response.

## 7. Database Development

SQLite was used as the database.

SQLAlchemy was used for database operations.

The database supports storing:

- User information
- Recommendation plans
- Recommendation history

## 8. Frontend Development

The frontend was developed using:

- HTML
- CSS
- JavaScript
- Jinja2 templates

The application includes pages for:

- Home
- Login
- Registration
- Dashboard
- Home Planner
- Party Planner
- Jewelry Planner
- Recommendations
- History

## 9. Project Structure

The main application structure is:

```text
app/
├── ai/
├── routers/
├── services/
├── auth.py
├── config.py
├── database.py
├── main.py
├── models.py
└── schemas.py

data/
static/
templates/
tests/
uploads/
## 10. Development Result

The development phase produced a functional PocketSmart AI web application with:

- User authentication
- Multiple planning modules
- Budget-aware recommendation generation
- AI integration
- Recommendation history
- Web-based user interface

The completed application can be executed locally using FastAPI and Uvicorn.