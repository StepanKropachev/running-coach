from ..utils import PromptTemplate

TRAINING_PLAN = PromptTemplate(
    template="""Based on user's goal: {user_goal}{context}

Generate a realistic training plan and explain key points."""
)
