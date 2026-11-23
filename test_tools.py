from datetime import date, timedelta

from tools import days_until_exam, split_study_hours


def test_days_until_exam():
    future_date = (date.today() + timedelta(days=10)).isoformat()
    assert days_until_exam.invoke({"exam_date": future_date}) == (
        "You have 10 days until your exam."
    )


def test_split_study_hours():
    result = split_study_hours.invoke({
        "total_hours": 6,
        "subjects": "Maths, Physics, Chemistry",
    })
    assert "Maths: 2.00 hours" in result
    assert "Physics: 2.00 hours" in result
    assert "Chemistry: 2.00 hours" in result


def test_invalid_exam_date():
    result = days_until_exam.invoke({"exam_date": "next Friday"})
    assert "Invalid date" in result


def test_invalid_study_hours():
    result = split_study_hours.invoke({
        "total_hours": 0,
        "subjects": "Maths",
    })
    assert "greater than zero" in result
