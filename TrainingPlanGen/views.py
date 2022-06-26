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
from units import scaled_unit
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

def activities(request):
    social = request.user.social_auth.get(provider='strava')
    token = social.extra_data['access_token']
    # get activity details
    client = Client()
    client.access_token = token
    query = client.get_activities(limit=20)
    activities = []
    km = scaled_unit('km', 'm', 1000)
    for activity in query:
            
            activities.append(
                { 
                    "id": activity.id,
                    "name": activity.name,
                    "distance": float(km(activity.distance)),
                    "type": activity.type,
                    "link": "https://www.strava.com/activities/{}".format(activity.id),
                    "date": activity.start_date_local.strftime("%b %e %a - %I:%M %p"),
                }
            )
    pprint(activities)
    return JsonResponse(activities, safe=False)