# Intelligent Meeting Assistant

A multi-agent system built with Microsoft AutoGen 0.4 for processing meeting recordings. The system transcribes audio, summarizes content, and extracts action items from meetings.

## Features

- **Audio Transcription**: Converts meeting audio into text using Azure Speech-to-Text
- **Meeting Summarization**: Generates concise summaries using OpenAI GPT models
- **Action Item Extraction**: Identifies tasks, assignees, and deadlines from meeting discussions
- **Agent Coordination**: Uses Microsoft AutoGen 0.4 for agent communication and orchestration
- **Modern Web Interface**: Clean, responsive UI with drag-and-drop file upload
- **Docker Support**: Easy deployment with Docker and docker-compose

## Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd intelligent-meeting-assistant
   ```

2. Create a `.env` file with your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   AZURE_SPEECH_KEY=your_azure_speech_key
   ```

3. Start the application with Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Visit `http://localhost:8000` in your browser

## Manual Installation

1. Ensure you have Python 3.8+ and ffmpeg installed

2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd intelligent-meeting-assistant
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export AZURE_SPEECH_KEY=your_azure_speech_key
   ```

6. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

## Development

### Project Structure

```
intelligent-meeting-assistant/
├── app.py                 # FastAPI web application
├── orchestrator.py        # Main orchestrator for agent coordination
├── transcription_agent.py # Audio transcription agent
├── summarization_agent.py # Text summarization agent
├── action_item_extraction_agent.py # Action item extraction agent
├── static/               # Static assets
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
├── templates/           # HTML templates
├── tests/              # Test files
├── uploads/            # Temporary file storage
└── docker-compose.yml  # Docker Compose configuration
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests with coverage
pytest --cov=./ --cov-report=term-missing
```

### Code Quality

```bash
# Install development dependencies
pip install black flake8 isort

# Format code
black .
isort .

# Check code quality
flake8 .
```

## API Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

[MIT License](LICENSE)

## Acknowledgments

- [Microsoft AutoGen](https://github.com/microsoft/autogen)
- [OpenAI](https://openai.com)
- [Azure Speech Services](https://azure.microsoft.com/services/cognitive-services/speech-services/) 