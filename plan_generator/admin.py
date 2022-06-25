from django.contrib import admin

from .models import Activity, Day, Week, TrainingPlan

# Register your models here.
admin.site.register(Week)
admin.site.register(TrainingPlan)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "day", "distance", "duration", "ascent")
    exclude = ("day", )


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ("date", "distance", "time", "ascent")
