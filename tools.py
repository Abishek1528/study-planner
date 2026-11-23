from datetime import date

from langchain_core.tools import tool


@tool
def days_until_exam(exam_date: str) -> str:
    """Calculate how many days remain until an exam date in YYYY-MM-DD format."""
    try:
        target_date = date.fromisoformat(exam_date.strip())
        remaining_days = (target_date - date.today()).days

        if remaining_days > 0:
            return f"You have {remaining_days} days until your exam."
        if remaining_days == 0:
            return "Your exam is today!"
        return f"Your exam date was {-remaining_days} days ago."
    except (AttributeError, ValueError):
        return "Invalid date. Please use YYYY-MM-DD format."


@tool
def split_study_hours(total_hours: float, subjects: str) -> str:
    """Divide total study hours equally among comma-separated subjects."""
    try:
        hours = float(total_hours)
        subject_list = [
            subject.strip()
            for subject in subjects.split(",")
            if subject.strip()
        ]

        if hours <= 0:
            return "Please enter study hours greater than zero."
        if not subject_list:
            return "Please provide at least one subject."

        each_subject = hours / len(subject_list)
        result = "Your study timetable:\n"
        for subject in subject_list:
            result += f"{subject}: {each_subject:.2f} hours\n"
        return result
    except (AttributeError, TypeError, ValueError):
        return "Please enter valid study hours and subjects."


TOOLS = [days_until_exam, split_study_hours]
TOOL_BY_NAME = {tool.name: tool for tool in TOOLS}
