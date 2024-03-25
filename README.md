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
[`POST /api/google-login`](#google-login): Receives log-in data from Google Log-in\
[`GET /api/get-nhl`](#get-nhl): Gets sports data from various sports\
[`PUT /api/add-fav`](#add-fav): Add team to user's favourites \
[`GET /get-follow`](#get-follow): Gets all followed teams for user dashboard 

