"""TrainingPlanGen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .views import ActivitiesView, ActivityView, CreateActivity, PlanView, import_activities, LogView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("oauth/", include('social_django.urls', namespace='social')),
    path("plan/", include("training_plan.urls")),
    path("activities/", ActivitiesView.as_view(), name='activities'),
    path("plan-view/", PlanView.as_view(), name="plan_view"),
    path("log-view/", LogView.as_view(), name="log_view"),
    path("activities/<int:pk>/", ActivityView.as_view(), name="activity_detail"),
    path("activities/create/", CreateActivity.as_view(), name="activity_create"),
    path("strava-activities/", import_activities, name="strava_activities")
]
