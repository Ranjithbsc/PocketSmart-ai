# Phase 2 – Requirement Analysis

## 1. Functional Requirements

The system should provide the following functionalities:

- User registration and login
- User authentication using sessions
- Dashboard for accessing different planners
- Home Interior Planner
- Party Planner
- Jewelry Planner
- Budget input and validation
- User requirement collection
- AI-based recommendation generation
- Budget allocation and breakdown
- Recommendation result display
- Recommendation history
- Viewing previously generated plans

## 2. Non-Functional Requirements

The application should satisfy the following requirements:

- Simple and user-friendly interface
- Fast response for normal application operations
- Secure handling of user authentication
- Proper input validation
- Maintainable project structure
- Responsive web interface
- Protection of sensitive configuration such as API keys
- Reliable database storage

## 3. User Requirements

Users should be able to:

1. Create an account.
2. Login securely.
3. Select a planning category.
4. Enter their budget and requirements.
5. Generate recommendations.
6. View the recommended plan and budget allocation.
7. Access previous recommendation history.

## 4. System Requirements

### Software Requirements

- Python 3.x
- FastAPI
- Uvicorn
- Jinja2
- SQLAlchemy
- SQLite
- Google Gemini API
- HTML5
- CSS3
- JavaScript
- Git and GitHub

### Hardware Requirements

- Computer/Laptop
- Minimum 4 GB RAM
- Internet connection for AI-based recommendations
- Modern web browser

## 5. Main Modules

### Authentication Module
Handles user registration, login and session-based authentication.

### Planner Module
Provides separate planners for:

- Home Interior
- Party
- Jewelry

### Recommendation Module
Processes user requirements and generates suitable recommendations.

### Catalog Module
Provides product/service information used for recommendation planning.

### History Module
Stores and displays previously generated recommendation plans.

## 6. Input Requirements

The system may collect information such as:

- User details
- Budget
- Planning category
- User preferences
- Requirements
- Occasion-related information
- Product preferences

## 7. Output Requirements

The system should provide:

- Recommended items/services
- Budget allocation
- Total estimated budget
- Recommendation details
- Saved recommendation history

## 8. Requirement Analysis Summary

The requirement analysis defines the functional, non-functional, user, hardware and software requirements needed to develop PocketSmart AI.

These requirements provide the foundation for the design and development phases of the project