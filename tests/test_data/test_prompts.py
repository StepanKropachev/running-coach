from llm.prompts.templates import TRAINING_PLAN, WORKOUT_ANALYSIS

# Test workout analysis
workout_data = {
    "distance": "10km",
    "time": "50min",
    "avg_pace": "5:00/km",
    "heart_rate": "155bpm",
}
user_goal = "I want to run marathon under 4 hours"
context = "Last 5 workouts show steady 45-55min 10k runs"

analysis = WORKOUT_ANALYSIS.format(
    workout_data=workout_data, user_goal=user_goal, context=context
)
print("Workout Analysis Template:\n", analysis, "\n")

# Test training plan
plan = TRAINING_PLAN.format(
    user_goal="I want to run my first marathon this spring",
    context="Current weekly mileage: 30km",
)
print("Training Plan Template:\n", plan)
