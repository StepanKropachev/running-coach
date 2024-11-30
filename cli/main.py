import typer
from rich import print

app = typer.Typer()


@app.command()
def analyze(workout_id: str):
    """Analyze a specific workout."""
    print(f"Analyzing workout: {workout_id}")


@app.command()
def plan(race: str, date: str):
    """Generate a training plan."""
    print(f"Generating plan for {race} on {date}")


if __name__ == "__main__":
    app()
