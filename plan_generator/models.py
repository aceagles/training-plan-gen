from django.db import models
from django.db.models import Sum

# Create your models here


class TrainingPlan(models.Model):

    start_volume = models.FloatField()


class Week(models.Model):

    start_date = models.DateField()


class Day(models.Model):
    """
    Prescribed training day.

    Will correspond to a single week.
    Can have many activities assigned to it.
    """

    date = models.DateField()
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
    start_time = models.DateTimeField()
    duration = models.DurationField()
    distance = models.FloatField()
    ascent = models.FloatField()
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="activities")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.day.update_totals()


class StravaActivity(Activity):
    url = models.URLField()
