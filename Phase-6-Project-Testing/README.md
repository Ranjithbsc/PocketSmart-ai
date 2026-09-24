# Phase 6 – Project Testing

## 1. Testing Overview

The PocketSmart AI application was tested to verify the functionality, reliability and usability of the developed modules.

Testing was performed on the main application features including authentication, planners, recommendation generation, database operations and web pages.

## 2. Authentication Testing

The authentication module was tested for:

- User registration
- User login
- Invalid login credentials
- Session handling
- Access to authenticated pages

## 3. Planner Testing

The following planners were tested:

- Home Interior Planner
- Party Planner
- Jewelry Planner

The planner forms were checked for correct input handling and request processing.

## 4. Recommendation Testing

Recommendation functionality was tested by providing different:

- Budget values
- Requirements
- Planner categories
- User preferences

The generated recommendation and budget breakdown were checked for proper display.

## 5. API Testing

The FastAPI endpoints were tested to verify:

- Correct request handling
- Input validation
- Successful responses
- Error handling

The application's API documentation was also verified using the FastAPI Swagger interface.

## 6. Database Testing

Database functionality was tested for:

- User data storage
- Recommendation storage
- Recommendation history
- Data retrieval

SQLite and SQLAlchemy operations were verified during application usage.

## 7. UI Testing

The web interface was tested for:

- Page navigation
- Login and registration pages
- Dashboard
- Planner pages
- Recommendation results
- History page
- Responsive layout
- Button and link functionality

## 8. Test Cases

| Test Case | Expected Result | Status |
|---|---|---|
| User Registration | New user account created | Passed |
| User Login | User successfully logged in | Passed |
| Dashboard Access | Dashboard displayed | Passed |
| Home Planner | Home planning form works | Passed |
| Party Planner | Party planning form works | Passed |
| Jewelry Planner | Jewelry planning form works | Passed |
| Recommendation Generation | Recommendation displayed | Passed |
| History | Previous plans displayed | Passed |
| API Documentation | Swagger UI accessible | Passed |
| Database Operations | Data stored and retrieved | Passed |

## 9. Error Handling

The application was checked for common errors such as:

- Invalid user input
- Missing required fields
- Incorrect login details
- API/service errors
- Invalid requests

Appropriate validation and error handling were implemented where required.

## 10. Testing Result

The main application features were tested successfully.

The testing phase confirmed that the major modules of PocketSmart AI work together as intended and that the application can be used for budget planning and recommendation generation.