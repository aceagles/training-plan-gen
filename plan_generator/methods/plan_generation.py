import math
from datetime import datetime, timedelta
from pprint import pprint


def generate_weekly_totals(
    peakDate, peakVolume, startVolume, startDate=datetime.now().date(), rampRate=0.1
):
    """
    Generate a ramping list of weeks for the training plan. Peaking at race peakDate
    """
    # Calculate the number of weeks until raceday
    startWeek = startDate - timedelta(days=startDate.weekday())
    endWeek = peakDate - timedelta(days=peakDate.weekday())
    weeks = int(((endWeek - startWeek).days + 1) / 7)

    # Calculate the ramp - 3 weeks up at ramp rate, 1 week half load, then 3 at ramp rate
    # If peak distance is reached keep steady

    week_list = []
    distance = startVolume
    weekCounter = 0
    for i in range(weeks):
        week = {}
        week['start_date'] = startWeek + timedelta(days=i*7)
        if weekCounter <= 2:
            week['distance'] = distance
            distance += distance * rampRate
            distance = math.floor(min(distance, peakVolume))
            weekCounter += 1
        else:
            week['distance'] = distance / 2
            weekCounter = 0
        week_list.append(week)
    return week_list


def generate_daily_distances(total, percent_list):
    """Scale the percentages in the event that they don't sum to 1. Return the volume and new percentages"""
    # Add to shortest day if percentages too few
    # TODO: scale second shortest day as well if the difference is too much
    if sum(percent_list) < 1:
        percent_list[percent_list.index(min(percent_list))] += 1 - sum(percent_list)
    # Take from longest day if too large
    if sum(percent_list) > 1:
        percent_list[percent_list.index(max(percent_list))] -= sum(percent_list) - 1

    return [round(total * x) for x in percent_list]


if __name__ == "__main__":
    endDate = datetime(2022, 10, 20).date()
    pprint(generate_weekly_totals(endDate, 100, 50))

    # print(list(generate_daily_distances(50, [0.5, 0.5, 0.1])))
