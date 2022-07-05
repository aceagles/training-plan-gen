import re

from django.shortcuts import render
from stravalib import Client

from TrainingPlanGen import settings


# Create your views here.
def authorize_redirect(request):
    client = Client()
    code = request.get("code")
    token_response = client.exchange_code_for_token(
        client_id=settings.STRAVA_ID, client_secret=settings.STRAVA_SECRET, code=code
    )
    profile = request.user.profile
    profile.access_token = token_response["access_token"]
    profile.refresh_token = token_response["refresh_token"]
    profile.expires_at = token_response["expires_at"]
