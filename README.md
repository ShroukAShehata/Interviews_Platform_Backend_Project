# Interviews Platform – Backend (Django)


##  Overview

A backend REST API for an **Interview Preparation & Knowledge Sharing Platform** built with **Django** and **Django REST Framework**.
The platform enables expert users to create and manage interview questions and answers, associate them with required skills, and the platform provides **analytics-driven insights** (top questions, trending questions, skills heatmap).

The project design includes these backend architecture principles (service layer, caching, rate-limit, signals, role-based auth)


##  Features

- Role-based profiles (Admin / Expert / Explorer)
- Question & answer management with ownership rules
- Skill-based tagging for interview questions
- Analytics Insights:
  * Top questions
  * Trending questions (time-decay scoring)
  * Skills heatmap
- Redis-backed caching with auto invalidation on models changing.
- Role-based & scoped API throttling
- Search, filtering, and ordering support for apis
- JWT authentication with refresh token rotation & blacklist
- Auto-generated OpenAPI / Swagger documentation


##  Tools Used

- Backend Framework: Django 5.2
- API Framework: Django REST Framework (DRF)
- Authentication: JWT (SimpleJWT + token blacklist)
- Database: SQLite (builtin db with django)
- Caching: Redis (django-redis)
- API Docs: Swagger
- Filtering & Search: django-filter, DRF filters
- Throttling: Custom role-based & scoped throttles



##  Authentication & Authorization

- JWT-based authentication using SimpleJWT
- Access & refresh tokens with rotation and blacklist
- Custom user model with a `role` field


##  API Overview

### Skills

* Create and manage skills
* Search and order by skill name

### Questions

* Experts/Admins can create questions
* Filter by category and difficulty
* Search by title and description
* Ownership-based update and delete

### Answers

* Only Experts/Admins can answer questions
* Ordered by votes and recency
* Ownership and role-based permissions

### Analytics

* **Top Questions:** Ranked by number of answers
* **Trending Questions:** Engagement-based scoring with time decay
* **Skills Heatmap:** Skill popularity based on question usage


##  Analytics & Caching Strategy

- Analytics results are cached in **Redis** to reduce database load
- Different TTLs are used depending on endpoint criticality
- **Django signals** automatically invalidate cache on:
  * Question creation/update
  * New answers submission


##  Throttling & Security

- Scoped throttling for write-heavy endpoints
- Role-based throttling limits (expert, explorer, admin)
- Separate limits for analytics endpoints
- Ownership checks using custom permissions


##  API Documentation

Interactive Swagger / OpenAPI documentation is available at:

/api/schema/
/api/docs/



