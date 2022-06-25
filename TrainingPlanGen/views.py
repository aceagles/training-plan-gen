from django.shortcuts import render
from django.views.generic import ListView
from plan_generator.models import Activity
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def index(request):
    return render(request, "TrainingPlanGen/index.html", {})



class ActivitiesView(LoginRequiredMixin, ListView):
    template_name = 'TrainingPlanGen/activities.html'
    paginate_by = 10
    model = Activity

    def get_queryset(self):
        return self.request.user.profile.activity.all().order_by('-start_time')