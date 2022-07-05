# training-plan-gen
A Django app to track and create training plans based loosely on uphill athlete methods

# Motivations and Scope
Whenever starting a new training block I sit down with a spreadsheet and plan out the next few months using a model
which slowly ramps and changes focus as time goes on.
I then fill out how my actual volume relates to my planned volume and adjust as required.

This project aims to automate all of this and also display the metrics in the way that I would like. 

The initial scope is:
- project to be serverside rendering as much as possible to leverage batteries included nature of django
- use hybrid django/react model for reactive components where they are required
- Create a day by day training plan based on a start volume, end volume and time period
- adjust the training plan as time goes on if targets are not met
- allow many users to use the site
- Pull activities from strava

A potential expanded scope is:
- build a DRF API
- Create a react frontend for nicer UX
