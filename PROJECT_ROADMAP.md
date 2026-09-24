# PocketSmart AI - Project Completion Roadmap

This roadmap is aligned to the supplied 39-page PocketSmart AI PDF. The PDF has an early Flask description, but its later FastAPI milestone and conclusion explicitly define FastAPI + Jinja2 as the final architecture. This implementation therefore uses FastAPI as the backend, while preserving the PDF's three planners and Gemini multimodal workflow.

## Milestone 1 - Gemini AI initialization
- Configure Gemini API access.
- Store the API key in `.env` only.
- Keep the model configurable (`GEMINI_MODEL`).
- Test text generation.
- Test text + image generation for Jewelry.
- Handle temporary Gemini failures with retries and a deterministic fallback.

## Milestone 2 - Core functionality
- Home planner: budget, rooms, lights, fans, furniture, dining, style, requirements.
- Party planner: budget, guests, event type, venue type, needs, requirements.
- Jewelry planner: budget, occasion, style, preferences, optional outfit image.
- Modular prompts and recommendation service.
- Catalog-backed product/service suggestions.
- Platform search links.

## Milestone 3 - FastAPI backend
- FastAPI application and startup initialization.
- `/api/generate-home`
- `/api/generate-party`
- `/api/generate-jewelry`
- `/register`, `/login/form`, `/logout`, `/token`
- `/api/session-info`
- `/api/history`
- `/api/recommendations/{id}`
- `/history`
- `/recommendations/{id}`
- CORS and session middleware.
- SQLite persistence.

## Milestone 4 - UI
- Landing page.
- Registration and login.
- Dashboard.
- Home planner form and recommendation cards.
- Party planner form and recommendation cards.
- Jewelry planner form with optional image upload.
- History page.
- Recommendation detail page.
- Responsive HTML/CSS/Jinja2/JavaScript.

## Milestone 5 - Testing and optimization
- Test health endpoint.
- Test public pages.
- Test registration/login/session.
- Test Home fallback generation.
- Test Party fallback generation.
- Test Jewelry fallback generation.
- Test image upload validation.
- Verify recommendations never exceed the user budget.
- Verify history is separated by logged-in user.
- Verify the app still runs when Gemini is unavailable.

## Final project demonstration checklist
1. Start server.
2. Open home page.
3. Register a new account.
4. Login.
5. Generate a Home plan with a normal budget such as 50000.
6. Generate a Party plan.
7. Generate a Jewelry plan without image.
8. Generate a Jewelry plan with a JPEG/PNG/WebP image.
9. Open History.
10. Open a saved recommendation.
11. Open `/docs` and show the FastAPI endpoints.
12. Open `/health` and show `status: ok`.

## Scope note from the PDF
The PDF describes Amazon, Flipkart, IKEA, Swiggy, Zomato, OYO and other platforms. This starter implementation uses a local mock catalog plus platform search URLs so it does not invent live price/stock data. Live partner APIs or approved data integrations can be added as a separate production phase.
