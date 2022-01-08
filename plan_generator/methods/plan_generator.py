from datetime import timedelta,datetime

def generate_weekly_totals(peakDate, peakVolume, startVolume, startDate = datetime.now(), rampRate = 0.1):
    """
    Generate a ramping list of weeks for the training plann. Peaking at race day.
    """
    # Calculate the number of weeks until raceday
    startWeek = startDate - timedelta(days=startDate.weekday())
    endWeek = peakDate - timedelta(days=peakDate.weekday())
    weeks = int(((endWeek - startWeek).days +1 )/7)
    
    # Calculate the ramp - 3 weeks up at ramp rate, 1 week half load, then 3 at ramp rate
    # If peak distance is reached keep steady
    
    distances = []
    distance = startVolume
    weekCounter = 0
    for i in range(weeks):
        if weekCounter <=2:
            distances.append(distance)
            distance += distance * rampRate
            weekCounter += 1
        else:
            distances.append(distance/2)
            weekCounter = 0
    return distances

def generate_daily_distances(total, percent_list):
    """Scale the percentages in the event that they don't sum to 1. Return the volume and new percentages"""
    # Add to shortest day if percentages too few
    # TODO: scale second shortest day as well if the difference is too much
    if sum(percent_list) < 1:
        percent_list[percent_list.index(min(percent_list))] += 1 - sum(percent_list) 
    # Take from longest day if too large
    if sum(percent_list) > 1:
        percent_list[percent_list.index(max(percent_list))] -= sum(percent_list) - 1
        
    return zip(percent_list,[total * x for x in percent_list])
        

    
if __name__ == "__main__":

    endDate = datetime(2021, 9, 20)
    generate_weekly_totals(endDate, 100,50)
    print(list(generate_daily_distances(50, [0.5, 0.5, 0.1])))