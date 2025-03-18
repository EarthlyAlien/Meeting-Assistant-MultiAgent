import os
import tempfile
import shutil
from pathlib import Path

import pytest

from meeting_assistant.config import (
    AgentConfig,
    AppConfig,
    AutoGenConfig,
    WorkspaceConfig,
)
from meeting_assistant.orchestrator import MeetingAssistantOrchestrator


@pytest.fixture
def mock_audio_file():
    """Create a temporary mock audio file for testing"""
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_file.close()
    yield temp_file.name
    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)


@pytest.fixture
def test_config():
    """Create a test configuration"""
    agent_config = AgentConfig(
        openai_api_key="test_openai_key",
        azure_speech_key="test_azure_key",
        model_name="gpt-4",
        temperature=0.7,
        max_tokens=1000,
    )

    workspace_config = WorkspaceConfig(
        upload_dir=Path("test_uploads"),
        results_dir=Path("test_results"),
        temp_dir=Path("test_temp"),
    )

    autogen_config = AutoGenConfig(
        use_docker=False,
        max_consecutive_auto_reply=5,
        human_input_mode="NEVER"
    )

    return AppConfig(
        agent=agent_config,
        workspace=workspace_config,
        autogen=autogen_config,
        debug=True,
        log_level="DEBUG",
    )


@pytest.fixture
def test_dirs(test_config):
    """Create and clean up test directories"""
    # Create test directories
    test_config.workspace.upload_dir.mkdir(parents=True, exist_ok=True)
    test_config.workspace.results_dir.mkdir(parents=True, exist_ok=True)
    test_config.workspace.temp_dir.mkdir(parents=True, exist_ok=True)

    yield test_config.workspace

    # Clean up test directories
    for dir_path in [
        test_config.workspace.upload_dir,
        test_config.workspace.results_dir,
        test_config.workspace.temp_dir,
    ]:
        if dir_path.exists():
            shutil.rmtree(dir_path)


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    return {
        "api_key": "test_key",
        "model": "gpt-4-turbo-preview",
        "output_dir": "test_output",
        "temp_dir": "test_temp",
        "use_docker": False,
        "timeout": 300
    }


@pytest.fixture
def orchestrator(mock_config):
    """Create an orchestrator instance for testing."""
    return MeetingAssistantOrchestrator(mock_config)


@pytest.fixture
def sample_results():
    """Create sample results for testing."""
    return {
        "transcription": (
            "Sample meeting transcription with multiple "
            "lines of text for testing purposes"
        ),
        "summary": "Sample meeting summary",
        "action_items": {
            "action_items": [
                {
                    "task": "Test task",
                    "assignee": "John",
                    "due_date": "2024-03-15"
                }
            ]
        },
        "metadata": {
            "audio_file": "test.wav",
            "timestamp": "2024-03-01 12:00:00"
        }
    }
