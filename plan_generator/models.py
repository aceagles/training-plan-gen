from pyexpat import model
from django.db import models
from django.db.models import Sum
from account.models import Profile
from toolkit.time_funcs import get_part_of_day

# Create your models here


class TrainingPlan(models.Model):
    class VolMetric(models.TextChoices):
        TIME = "TIME", "Time" 
        DISTANCE = "DISTANCE", "Distance"
        ASCENT = "ASCENT", "Ascent"
    
    start_volume = models.FloatField()
    end_volume = models.FloatField()
    volume_metric = models.CharField(max_length=30, choices=VolMetric.choices)


class Week(models.Model):
    """
    Prescribed training week.

    Will correspond to a single plan and user.
    Will have many days assigned to it.
    
    """
    start_date = models.DateField(unique=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="weeks", null=True)
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name="weeks", null=True)
    plan_distance = models.FloatField()
    plan_time = models.FloatField()
    distance = models.FloatField()
    time = models.FloatField()



class Day(models.Model):
    """
    Prescribed training day.

    Will correspond to a single week.
    Can have many activities assigned to it.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="days", null=True)
    date = models.DateField(unique=True)
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="days")
    plan_distance = models.FloatField()
    plan_time = models.FloatField()
    distance = models.FloatField()
    time = models.DurationField()
    ascent = models.FloatField()

    def update_totals(self):
        self.time = self.activities.aggregate(Sum("duration"))["duration__sum"]
        self.distance = self.activities.aggregate(Sum("distance"))["distance__sum"]
        self.ascent = self.activities.aggregate(Sum("ascent"))["ascent__sum"]
        self.save()

    def __str__(self):
        return self.date.strftime("%d/%m/%Y")


class Activity(models.Model):
    class ActivityChoices(models.TextChoices):
        RUN = "Run", "Run"
        RIDE = "Ride", "Ride"
        WALK = "Walk", "Walk"


    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="activity")
    start_time = models.DateTimeField()
    duration = models.DurationField()
    distance = models.FloatField()
    ascent = models.FloatField()
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="activities", null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    activity_type = models.CharField(max_length=30, 
        choices=ActivityChoices.choices, 
        default=ActivityChoices.RUN)
    
    def save(self, *args, **kwargs):
        if not self.day:
            print(self.profile.days.all())
            tmp_day = self.profile.days.get(date = self.start_time.date())
            if tmp_day is not None:
                self.day = tmp_day
        if not self.name:
            part_day = get_part_of_day(self.start_time.hour)
            self.name = f"{part_day} {self.activity_type}"
        super().save(*args, **kwargs)
        self.day.update_totals()


