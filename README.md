# CalculatorPro – Full-Stack Django Calculator Application
`Deployment: Live frontend and backend deployed. You can access and use the application by visiting the Deployment Details section given below.`


**A professional, full-stack calculator application built with Django REST Framework and Vue.js**, designed to demonstrate authentication, session management, REST APIs, guest access, and admin control — as required in the Django assessment.

---

## Assessment Overview

This project was developed as part of a **Django Technical Assessment** consisting of **four progressive phases**:

1. Basic calculator functionality
2. User authentication & REST APIs
3. Guest session support
4. Admin interface & testing readiness

The application evolves from a simple calculator into a **production-grade, role-aware system** supporting **guest users, authenticated users, session isolation, and administrative oversight**.

---

## 🔗 Deployment Details

- **Live App (Integrated):** [https://django-fastapi-learning-project.vercel.app/](https://django-fastapi-learning-project.vercel.app/)

## 🔗 Frontend and Backend Deployed Link
- **Vercel (Frontend):** `https://django-fastapi-learning-project.vercel.app/` 
- **Koyeb (Backend API):** `https://calculatorpro-django-backend.koyeb.app/` 
- **Cloud Database:** `PostgreSQL (Hosted on Render)` 

## 🔗 Admin Panel Access (For Evaluation)

The Django Admin panel is enabled for reviewer evaluation and verification of backend functionality.

* **Admin URL:**
  [https://calculatorpro-django-backend.koyeb.app/admin/](https://calculatorpro-django-backend.koyeb.app/admin/)

* **Admin Credentials (Temporary):**

  ```
  Username: admin
  Password: admin@123
  ```

> Note:
> The admin interface is configured in **read-only mode** for calculation records to prevent accidental data modification.
> These credentials are provided **only for assessment and review purposes** and can be rotated or disabled after evaluation.

---
## Application Overview

**CalculatorPro** allows users to perform mathematical operations while maintaining a detailed calculation history.

### Key Highlights

* Guest & Premium access modes
* Session-based guest history (isolated per user)
* Secure authentication for registered users
* RESTful API architecture
* Smart calculation notes
* Weekly analytics
* Admin dashboard with read-only data control

---

## Project Phases & Implementation

---

## Phase 1 – Basic Calculator Functionality 

### Features Implemented

* Two numeric input fields
* Operator selection:

  * Addition (+)
  * Subtraction (−)
  * Multiplication (×)
  * Division (÷)
* Real-time validation (division by zero handled)
* Calculation result storage in database
* History page displaying calculations

### Technologies Used

## Backend
* Django Models
* Django Views
* PostgreSQL Database
* Django 4.2
* Django ORM

## Frontend
* Vue 3
* Vite
* Axios
* Tailwind-style utility CSS

## Deployment
* Backend: Koyeb
* Frontend: Vercel
  
---

## Phase 2 – Authentication & REST API 

### Authentication

* User registration
* Login & logout
* Session-based authentication
* Secure CSRF handling



## API Endpoints (Phase 2)

```md
### Authentication APIs

| Method | Endpoint            | Description               | Access |
|--------|---------------------|---------------------------|--------|
| GET    | /api/auth/csrf/     | Sets CSRF cookie          | Public |
| POST   | /api/auth/register/ | Register new user         | Public |
| POST   | /api/auth/login/    | Login user                | Public |
| POST   | /api/auth/logout/   | Logout user            | Authenticated |
| GET    | /api/auth/me/       | Get auth status           | Public |

---

### Calculator APIs

| Method | Endpoint             | Description               |    Access     |
|--------|----------------------|---------------------------|---------------|
| POST   | /api/calculate/      | Perform a calculation     | Guest / Auth  |
| GET    | /api/history/        | Fetch calculation history | Guest / Auth  |
| DELETE | /api/history/clear/  | Clear all history         | Authenticated |
| DELETE | /api/history/<id>/   | Delete single record      | Authenticated |

---
```


### Guest Restrictions
- Maximum 10 calculations per session
- Notes allowed for only 2 calculations
- Cannot clear or delete history

### Authenticated User Privileges
- Unlimited calculations
- Unlimited notes
- Full history access
- Can delete individual records
- Can clear entire history
  
---

## Phase 3 – Guest Session Support 

### Guest Capabilities

* Use calculator **without login**
* Session-based history storage
* Session isolation:

  * Guest A sees only Guest A’s history
  * Guest B sees only Guest B’s history
* Parallel guest sessions supported
* Cookies + Django sessions used

### Guest Limitations

* Maximum **10 calculations**
* Can view history (read-only)
* Cannot:

  * Delete individual items
  * Clear full history
  * Permanently save data

---

## Phase 4 – Admin Interface & Testing Readiness ✅

### Django Admin Panel

* Admin login enabled
* View:

  * Registered users
  * All calculation histories
* **Read-only CalculationHistory model**

  * No delete or modify allowed from admin
* Clean admin UI

### Logging & Error Handling

* Input validation
* API error responses
* Graceful UI error messages

## Running Unit Tests

Unit tests are written using Django’s built-in testing framework.

### Test Coverage
- Calculation model creation
- Guest calculations
- Authenticated user calculations
- Fetching calculation history
- Clearing and deleting history

### Run Tests

```bash
cd backend
python manage.py test

```
---
## Access Modes


### Guest Users

**Capabilities**

* ▸ Basic calculator access
* ▸ View only the **last 10 calculations**
* ▸ Notes allowed on **maximum 2 calculations**
* ▸ Weekly usage analytics

**Restrictions**

* ▸ History deletion is **not permitted**
* ▸ Full history reset is **not allowed**
* ▸ Data is **session-based** and not permanently stored

---

### Authenticated (Premium) Users

**Capabilities**

* ▸ Unlimited calculator usage
* ▸ Full access to calculation history
* ▸ Unlimited notes on calculations
* ▸ Weekly usage analytics
* ▸ Delete individual calculation records
* ▸ Clear complete calculation history
* ▸ **Persistent storage** backed by database

---

## Smart Notes System

* Attach notes to calculations
* Useful for:

  * Business calculations
  * Financial planning
  * Learning & tracking
* Guest: limited notes
* Premium: unlimited notes

---

## Weekly Analytics

* Track number of calculations
* Weekly usage insights
* Available to both guest & premium users

---

## Tech Stack

| Layer    | Technology                     |
| -------- | ------------------------------ |
| Backend  | Django + Django REST Framework |
| Frontend | Vue.js 3                       |
| Database | PostgreSQL                     |
| Auth     | Django Session Authentication  |
| API      | REST (JSON)                    |
| UI Icons | Lucide Icons                   |
| State    | Cookies + Sessions             |

---

##  Project Setup

### Clone Repository

```bash
git clone https://github.com/coderiders22/django-fastapi-learning-project.git

```

---

### Backend Setup (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### Frontend Setup (Vue)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

##  Running Tests

```bash
python manage.py test
```

---

##  Database Schema (Core)

### `CalculationHistory`

| Field       | Type                  |
| ----------- | --------------------- |
| user        | ForeignKey (nullable) |
| session_key | CharField             |
| operand1    | Float                 |
| operand2    | Float                 |
| operator    | Char                  |
| result      | Float                 |
| created_at  | DateTime              |

### Notes
- For authenticated users, records are linked via a foreign key to the User model.
- For guest users, records are linked using Django session keys without creating user accounts.
- Django’s built-in `auth` and `session` tables are used internally and are not duplicated.

### Performance & Indexing Notes

- `user` and `session_key` fields are frequently used for filtering calculation history and are indexed implicitly via Django ORM.
- The schema is optimized for read-heavy operations such as history listing and admin review.
- Pagination is handled at the API level to avoid large result sets.

### Data Integrity Considerations

- Each calculation record is associated with **either** a registered user **or** a guest session.
- Guest calculations are isolated using Django's session framework without persisting temporary users.
- Input validation and operator safety checks are enforced at the API layer before persisting data.

### Design Decision: Single History Table

A single `CalculationHistory` table is used for both guest and authenticated users instead of maintaining separate tables.

---

## Security Considerations

* CSRF protection enabled
* Session-based authentication
* Permission-controlled endpoints
* Guest session isolation
* Admin access restricted

---

## Folder Structure (Simplified)

## 📁 Project Structure

The project is organized into two main parts: a Django REST backend and a Vue.js frontend.

### Frontend (Vue.js)

``` frontend/vue-calculator-ui/
├── public/
│   └── favicon.ico
│
├── src/
│   ├── assets/
│   │   ├── gradient.css      # Global gradient & theme styles
│   │   └── logo.svg
│   │
│   ├── components/
│   │   ├── Calculator.vue    # Core calculator UI + guest/premium logic
│   │   ├── History.vue       # Calculation history with access control
│   │   ├── Modal.vue         # Reusable modal (errors, warnings, success)
│   │   ├── Navbar.vue        # Auth-aware navigation bar
│   │   ├── Footer.vue        # Application footer
│   │   └── Logo.vue
│   │
│   ├── views/
│   │   ├── Welcome.vue       # Landing page (Guest vs Premium comparison)
│   │   ├── Dashboard.vue     # Calculator + History combined view
│   │   ├── Login.vue         # Login screen
│   │   ├── Register.vue      # Registration screen
│   │   └── NotFound.vue      # 404 page
│   │
│   ├── router/
│   │   └── index.js          # Vue Router configuration
│   │
│   ├── services/
│   │   └── api.js            # Axios instance (CSRF + session support)
│   │
│   ├── App.vue               # Root Vue component
│   └── main.js               # App bootstrap + CSRF initialization
│── index.html
├── package.json
├── package-lock.json
├── vercel.json
├── vite.config.js
└── node_modules/ 
```

### Backend (Django)

``` backend/
├── calculator/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py              # Admin configuration for CalculationHistory
│   ├── apps.py               # App configuration
│   ├── auth_views.py         # Session-based auth (login, register, logout, me, csrf)
│   ├── models.py             # CalculationHistory model
│   ├── serializers.py        # DRF serializers
│   ├── tests.py              # Test placeholders
│   ├── urls.py               # Calculator + Auth API routes
│   └── views.py              # Calculate, history, delete, clear logic
│
├── config/
│   ├── __init__.py
│   ├── asgi.py               # ASGI entry point
│   ├── settings.py           # Django settings (CORS, sessions, installed apps)
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI entry point
│
├── manage.py                 # Django management script
├── requirements.txt          # Backend dependencies
└── venv/                   # Python virtual environment (local)


```
---

---

## Admin Portal (Django Admin)

The project includes a fully functional **Django Admin Panel** for backend-level
management and evaluation.

### Admin URL
```

http://localhost:8000/admin/

```

### How to create Demo Admin Credentials
```

Admin Access (Local Development)

For local development, an admin user can be created using:
python manage.py createsuperuser

This is intended for development and testing purposes only.
In production, admin access is restricted and not exposed to end users.

```
# Then you have to set username and password for admin so as to access admin portal
* Username:
* Email address:
* Password:
* Password (again):
----
### Admin Capabilities

- View and manage all registered users
- Inspect all calculation history (guest + authenticated)
- Review operands, operators, results, timestamps
- Delete or audit calculation records
- Verify guest vs premium access behavior
- Backend-level data validation

### Why Admin Panel Matters

This demonstrates:
- Proper backend management practices
- Secure authentication handling
- Production-ready Django setup
- Ability to audit and control application data
---
## Screenshots (Demo)

| Screen | Preview |
|------|--------|
| Welcome Screen | ![Welcome](./Screenshots/welcome.png) |
| Guest Mode Dashboard | ![Guest Dashboard](./Screenshots/guest%20dashboard.png) |
| Guest History (Limited) | ![Guest History Limit](./Screenshots/guest%20history.png) |
| Guest Limit Reached     | ![Guest Limit](./Screenshots/guest%20limit.png) |
| Authentication Screen   | ![Login](./Screenshots/login.png) |
| Authentication Screen   | ![Register](./Screenshots/register.png) |
| Access Modes            | ![Guest vs Premium Access](./Screenshots/Guest%20vs%20Premium%20Access.png) |
| Premium User Dashboard | ![Premium Dashboard](./Screenshots/premium%20user.png) |
| Delete Single History Item | ![Premium user deleting an individual calculation](./Screenshots/delete%20single%20history.png)|
| Clear Entire History | ![Premium user clearing all calculation history at once](./Screenshots/clear%20all%20history.png)| 
| Premium Unlimited History Management | ![Premium Unlimited History](./Screenshots/Premium%20Unlimited%20History.png) |
| Add Notes | ![Adding notes to a calculation (Premium feature)](./Screenshots/add%20notes.png) |
| Calculation Notes | ![Notes](./Screenshots/calculation%20notes..png) |
| Weekly Analytics | ![Analytics](./Screenshots/analytics.png) |
| Django Admin Panel | ![Admin](./Screenshots/admin%20portal.png) |
| Django Admin Panel | ![Users List](./Screenshots/users%20admin.png) |
| Responsive for all screens | ![Fully responsive and optimized across desktop, tablet, and mobile devices](./Screenshots/IMG_0587.png) |

---

## Author

**Developed by:** Manav Rai  
**Institution:** Punjab Engineering College, Chandigarh  
**Email:** [manavrai454@gmail.com](mailto:manavrai454@gmail.com)  
**GitHub:** [github.com/coderiders22](https://github.com/coderiders22/)

---

## License

© 2026 **Manav Rai**
All rights reserved.

---
