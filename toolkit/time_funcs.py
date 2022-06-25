def get_part_of_day(h):
    return (
        "Morning"
        if 5 <= h <= 11
        else "Afternoon"
        if 12 <= h <= 17
        else "Evening"
        if 18 <= h <= 22
        else "Night"
    )