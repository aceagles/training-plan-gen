from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from plan_generator.models import Activity
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import edit
from django.urls import reverse_lazy
from datetime import datetime
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
        