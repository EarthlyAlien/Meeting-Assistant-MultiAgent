# Meeting Assistant - Multi-Agent System

A sophisticated multi-agent system built with Microsoft AutoGen 0.4 for processing meeting recordings. The system transcribes audio, summarizes content, and extracts action items from meetings using specialized agents.

## Author

**Chaitanya K.K. Vankadaru**

## Features

- **Audio Transcription**: Converts meeting audio into text using Azure Speech-to-Text
- **Meeting Summarization**: Generates concise summaries using OpenAI GPT models
- **Action Item Extraction**: Identifies tasks, assignees, and deadlines from meeting discussions
- **Agent Coordination**: Uses Microsoft AutoGen 0.4 for agent communication and orchestration
- **Robust Error Handling**: Comprehensive error handling and logging
- **Configurable**: Flexible configuration management using Pydantic
- **Well-Tested**: Extensive test coverage with pytest
- **CI/CD Ready**: GitHub Actions workflow for testing, linting, and security checks

## Installation

### Prerequisites

- Python 3.12
- FFmpeg (for audio processing)
- OpenAI API key
- Azure Speech Services key

### Using pip

```bash
# Clone the repository
git clone https://github.com/EarthlyAlien/Meeting-Assistant-MultiAgent.git
cd Meeting-Assistant-MultiAgent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
AZURE_SPEECH_KEY=your_azure_speech_key
MODEL_NAME=gpt-4  # Optional, defaults to gpt-4
TEMPERATURE=0.7   # Optional, defaults to 0.7
MAX_TOKENS=1000   # Optional, defaults to 1000
DEBUG=false       # Optional, defaults to false
LOG_LEVEL=INFO    # Optional, defaults to INFO
```

## Usage

### Basic Usage

```python
from meeting_assistant import MeetingAssistantOrchestrator

# Initialize the orchestrator
orchestrator = MeetingAssistantOrchestrator()

# Process a meeting recording
results = orchestrator.process_meeting("path/to/meeting.wav")

# Generate a report
report = orchestrator.generate_report(results)

# Save results
orchestrator.save_results(results, "meeting_results.json")
```

### Directory Structure

```
meeting_assistant/
├── __init__.py
├── config.py           # Configuration management
├── logger.py          # Logging setup
├── orchestrator.py    # Main orchestrator
├── transcription_agent.py
├── summarization_agent.py
└── action_item_extraction_agent.py

tests/
├── __init__.py
├── conftest.py        # Test configuration
└── test_orchestrator.py

logs/                  # Log files
results/              # Processing results
uploads/              # Uploaded audio files
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=./ --cov-report=term-missing

# Run specific test file
pytest tests/test_orchestrator.py -v
```

### Code Quality

```bash
# Format code
black .
isort .

# Check code quality
flake8 .
```

### Security Checks

```bash
# Install security tools
pip install bandit safety

# Run security checks
bandit -r .
safety check
```

## CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that:

1. Tests the code on multiple Python versions (3.9-3.12)
2. Checks code formatting (black, isort)
3. Runs linting (flake8)
4. Performs security checks (bandit, safety)
5. Builds and publishes Docker images
6. Reports test coverage

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Microsoft AutoGen](https://github.com/microsoft/autogen)
- [OpenAI](https://openai.com)
- [Azure Speech Services](https://azure.microsoft.com/services/cognitive-services/speech-services/) 
