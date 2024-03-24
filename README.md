# Score-Sphere #

Score-Sphere is a full-stack web application to display personalized real-time game stats and centralize sports updates.

## Technologies ##
- **Front-end:** React, CSS
- **Back-end:** Python, Django, PostgreSQL, AWS

## Features ##
- **User Authentication:** Secure sign-in using Google accounts
- **Dashboard Toggling:** Swap between a universal dashboard and personalized, user-favourited teams
- **Team Favouriting:** Modify favourite teams/players easily through search

## Back-end Documentation ##

### API Endpoints ###
[`GET /users`](#get-user-data): Get all user data. Optional ordering by name, email, and company; optional filtering by name. \
[`GET /users/<int:user_id>`](#get-users-by-id): Gets user info by ID. \
[`PUT /users/<int:user_id>`](#update-user-info): Updates user info by ID. \
[`GET /insert-data`](#insert-data): Resets tables and inserts data according to selected JSON. \
[`POST /register`](#register): Registers a new user. \
[`GET /skills`](#get-skills): Get all skills data. Optional filtering by frequency and name. \
[`GET /skills/<str:skill_name>`](#get-skill-by-name): Get users associated with skill. Optional ordering by rating. 
