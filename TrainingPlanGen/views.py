from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from plan_generator.models import Activity, Week
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import edit
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.http import JsonResponse
from pprint import pprint
from stravalib import Client
from social_django.utils import load_strategy
from units import scaled_unit
from django.shortcuts import redirect
import time
from django.db.models import Sum
# Create your views here.


def index(request):
    return render(request, "TrainingPlanGen/index.html", {})



class ActivitiesView(LoginRequiredMixin, ListView):
    template_name = 'TrainingPlanGen/activities.html'
    paginate_by = 10
    model = Activity

    def get_queryset(self):
        return self.request.user.profile.activity.all().order_by('-start_time')

class ActivityView(LoginRequiredMixin, DetailView):
    template_name = "TrainingPlanGen/activity_detail.html"
    model = Activity

class CreateActivity(edit.CreateView):
    model = Activity
    fields = ("name", "duration", "distance", "ascent", "activity_type")
    template_name = "TrainingPlanGen/activity_create.html"

    def get_success_url(self) -> str:
        return reverse_lazy('activity_detail', kwargs={"pk": self.object.pk})
    
    def form_valid(self, form):
        form.instance.start_time = datetime.now()
        form.instance.profile = self.request.user.profile       
        return super().form_valid(form)

class PlanView(LoginRequiredMixin, ListView):
    template_name = "TrainingPlanGen/plan_view.html"
    paginate_by = 10
    model = Week

    def get_queryset(self):
        start_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
        return self.request.user.profile.weeks.filter(start_date__gte=start_week).order_by('start_date')
    
    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        data['plan'] = self.request.user.profile.trainingplan
        return data

class LogView(LoginRequiredMixin, ListView):
    template_name = "TrainingPlanGen/log_view.html"
    paginate_by = 10
    model = Week

    def get_queryset(self):
        log_weeks = self.request.user.profile.weeks.filter(start_date__lte = datetime.now().date()).order_by('-start_date')
        return log_weeks

def import_activities(request):
    # Get access token and refresh if required.
    social = request.user.social_auth.get(provider='strava')
    if social.extra_data['expires'] < int(time.time()):
        strategy = load_strategy()
        social.refresh_token(strategy)
    token = social.extra_data['access_token']
    # get activity details
    client = Client()
    client.access_token = token
    query = client.get_activities(limit=20)
   
    km = scaled_unit('km', 'm', 1000)
    for activity in query:
        # Delete activity if it has the same strava id.
        # this is to update the activity if it has changed since
        # last import
        try:
            act = request.user.profile.activity.get(strava_id=activity.id)
            act.delete()
        except Activity.DoesNotExist:
            pass
        # Create new activity
        strava_activity = Activity(
            profile = request.user.profile,
            start_time = activity.start_date,
            duration = activity.elapsed_time,
            distance = float(km(activity.distance)),
            ascent = activity.total_elevation_gain,
            name = activity.name,
            activity_type = activity.type,
            strava_id = activity.id
        )
        strava_activity.save()
            
    return redirect('activities')