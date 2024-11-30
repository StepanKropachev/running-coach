# AI Running Coach

AI-powered running coach that provides personalized training plans and workout analysis.

## Features

- Strava integration for workout tracking
- AI-powered workout analysis
- Personalized training plan generation
- Command-line interface for easy interaction

## Installation

```bash
pip install running-coach
```

## Quick Start

1. Set up Strava authentication:
```bash
running-coach auth strava
```

2. Generate a training plan:
```bash
running-coach plan create --race marathon --date 2024-09-01
```

3. Analyze your last workout:
```bash
running-coach analyze last-workout
```

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd running-coach
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix/macOS:
source .venv/bin/activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Initialize pre-commit hooks:
```bash
pre-commit install
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
