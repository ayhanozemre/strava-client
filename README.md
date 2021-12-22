# - Strava Basic Client


This is a simple Strava client. Currently it has two views which uses the leaderboards data.

# How does it work ?
  - create strava application
  - pip install -r requirements.txt
  - set the secret key of your application in env to the variable STRAVA_SECRET_KEY
  - python manage.py

# Endpoints
  - uri : /leaderboard-intersection
  - description : This view returns the intersection of riders who appear on multiple popular segments.
---
  - uri : /leaderboard-ontersection-scores
  - description : This view creates the score information for leaderboard-intersection view.


# Score Calculation
While calculation score, riders' rank, their metres-per-second data and total watts spent per hour is used and an integer value is returned for each entry.
If the rider has multiple entries, then integer values for each entry is added together and it gives us their score.