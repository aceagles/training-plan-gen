from datetime import datetime

from plan_generator.methods import plan_generation


def test_10_weeek():
    startDate = datetime(2022, 1, 8)
    endDate = datetime(2022, 3, 20)
    output = [50, 55, 60, 33.0, 66, 72, 79, 43.0, 86, 94]

    assert plan_generation.generate_weekly_totals(endDate, 100, 50, startDate) == output
