from ..utils import PromptTemplate

WORKOUT_ANALYSIS = PromptTemplate(
    template="""Workout data: {workout_data}
User's goal: {user_goal}{context}

Analyze this workout and provide actionable insights."""
)
