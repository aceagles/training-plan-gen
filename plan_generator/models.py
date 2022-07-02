from datetime import timedelta
from pyexpat import model
from django.db import models
from django.db.models import Sum
from account.models import Profile
from toolkit.time_funcs import get_part_of_day
import plan_generator.methods.plan_generation as plan_gen
# Create your models here


class TrainingPlan(models.Model):
    class VolMetric(models.TextChoices):
        TIME = "TIME", "Time" 
        DISTANCE = "DISTANCE", "Distance"
        ASCENT = "ASCENT", "Ascent"
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    start_volume = models.FloatField()
    end_volume = models.FloatField()
    end_volume = models.FloatField(default=0.1)
    volume_metric = models.CharField(max_length=30, choices=VolMetric.choices)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.profile}'s Training Plan"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        weeks = plan_gen.generate_weekly_totals(self.end_date, 
                                                self.end_volume,
                                                self.start_volume,
                                                self.start_date)
        for week in weeks:
            # TODO - Update weeks here if they already exist
            week_obj = Week(start_date=week['start_date'],
                            profile = self.profile,
                            plan = self,
                            plan_distance = week['distance'],
                            plan_time = timedelta(minutes=6*week['distance']),
                            distance=0,
                            time=timedelta())
            week_obj.save()
        


class Week(models.Model):
    """
    Prescribed training week.

    Will correspond to a single plan and user.
    Will have many days assigned to it.
    
    """
    start_date = models.DateField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="weeks", null=True)
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name="weeks", null=True)
    plan_distance = models.FloatField(default = 0)
    plan_time = models.DurationField(default = timedelta())
    distance = models.FloatField(default = 0)
    time = models.DurationField(default = timedelta())


    def save(self, *args, **kwargs):
        try:
            prev_dat = self.profile.weeks.get(start_date = self.start_date)
            prev_dat.delete()
        except Week.DoesNotExist:
            pass
        super().save(*args, **kwargs)

        # Create all the days for the week TODO: Make a function for better calculatin the spread
        days = plan_gen.generate_daily_distances(self.plan_distance, [0, 0.2, 0.2, 0.05, 0.15, 0.3, 0.1])
        # TODO: Update days here if they already exist.
        for i, distance in enumerate(days):
            day_obj = Day(
               profile=self.profile,
                week=self,
                date= self.start_date + timedelta(days=i*1),
                plan_distance=distance
            )
            day_obj.save()


class Day(models.Model):
    """
    Prescribed training day.

    Will correspond to a single week.
    Can have many activities assigned to it.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="days", null=True)
    date = models.DateField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="days")
    plan_distance = models.FloatField(default=0)
    plan_time = models.FloatField(default=0)
    distance = models.FloatField(default=0)
    time = models.DurationField(default=timedelta())
    ascent = models.FloatField(default=0)

    @property
    def foot_dist(self):
        foot_dist = self.activities.filter(
            models.Q(activity_type="Run") | 
            models.Q(activity_type="Walk") | 
            models.Q(activity_type="Hike")).aggregate(models.Sum("distance")) 
        print(foot_dist)
        if foot_dist['distance__sum'] is not None:
            return foot_dist['distance__sum']
        else:
            return 0
    
    @property
    def ride_dist(self):
        foot_dist = self.activities.filter(
            activity_type = "Ride").aggregate(models.Sum("distance")) 
        if foot_dist['distance__sum'] is not None:
            return foot_dist['distance__sum']
        else:
            return 0

    def update_totals(self):
        self.time = self.activities.aggregate(Sum("duration"))["duration__sum"]
        self.distance = self.activities.aggregate(Sum("distance"))["distance__sum"]
        self.ascent = self.activities.aggregate(Sum("ascent"))["ascent__sum"]
        self.save()

    def __str__(self):
        return self.date.strftime("%d/%m/%Y")

    def save(self, *args, **kwargs):
        #Days must have unique dates. If one already exists then overwrite
        week_start = self.date - timedelta(days=self.date.weekday())
        try:
            wk = self.profile.weeks.get(start_date = week_start)
        except Week.DoesNotExist:
            wk = Week(
                profile = self.profile,
                start_date = week_start,
            )
            wk.save()
            print("new week")
        else:
            self.week = wk
        super().save(*args, **kwargs)


class Activity(models.Model):
    class ActivityChoices(models.TextChoices):
        RUN = "Run", "Run"
        RIDE = "Ride", "Ride"
        WALK = "Walk", "Walk"
        HIKE = "Hike", "Hike"


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
    strava_id = models.BigIntegerField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        #delete other activities if they have the same strava id
        if self.strava_id:
            dup_acts = self.profile.activity.filter(strava_id = self.strava_id)
            [act.delete() for act in dup_acts]
        
        # find or create a day for this activity to belong to
        try:
            tmp_day = self.profile.days.get(date = self.start_time.date())
        except Day.DoesNotExist:
            tmp_day = Day(profile = self.profile, date = self.start_time.date())
            tmp_day.save()
        self.day = tmp_day
        
        # Name activity if left blank
        if not self.name:
            part_day = get_part_of_day(self.start_time.hour)
            self.name = f"{part_day} {self.activity_type}"
        
        super().save(*args, **kwargs)
        
        if self.day is not None:
            self.day.update_totals()


