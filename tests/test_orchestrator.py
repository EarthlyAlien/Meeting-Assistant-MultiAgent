import os
import tempfile
import pytest
from pathlib import Path
from orchestrator import MeetingAssistantOrchestrator

@pytest.fixture
def mock_audio_file():
    """Create a temporary mock audio file for testing"""
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_file.close()
    yield temp_file.name
    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)

@pytest.fixture
def orchestrator():
    """Create an orchestrator instance for testing"""
    config = {
        "openai_api_key": "test_openai_key",
        "azure_speech_key": "test_azure_key"
    }
    return MeetingAssistantOrchestrator(config)

def test_orchestrator_initialization(orchestrator):
    """Test that the orchestrator initializes correctly"""
    assert orchestrator.config["openai_api_key"] == "test_openai_key"
    assert orchestrator.config["azure_speech_key"] == "test_azure_key"
    assert orchestrator.transcription_agent is not None
    assert orchestrator.summarization_agent is not None
    assert orchestrator.action_item_extraction_agent is not None

def test_process_meeting(orchestrator, mock_audio_file):
    """Test the meeting processing workflow"""
    results = orchestrator.process_meeting(mock_audio_file)
    
    # Check that all components are present in results
    assert "transcription" in results
    assert "summary" in results
    assert "action_items" in results
    
    # Check metadata
    assert "metadata" in results["transcription"]
    assert "metadata" in results["summary"]
    assert "metadata" in results["action_items"]

def test_generate_report(orchestrator):
    """Test report generation"""
    # Mock results
    results = {
        "transcription": {
            "transcription": "Test transcription",
            "metadata": {"status": "completed"}
        },
        "summary": {
            "summary": "Test summary",
            "metadata": {"status": "completed"}
        },
        "action_items": {
            "action_items": [
                {
                    "task": "Test task",
                    "assignee": "John",
                    "deadline": "tomorrow"
                }
            ],
            "metadata": {"status": "completed"}
        }
    }
    
    report = orchestrator.generate_report(results)
    
    # Check that report contains all sections
    assert "# Meeting Assistant Report" in report
    assert "## Meeting Summary" in report
    assert "## Action Items" in report
    assert "## Full Transcription" in report
    
    # Check content
    assert "Test summary" in report
    assert "Test task" in report
    assert "John" in report
    assert "Test transcription" in report

def test_save_results(orchestrator, tmp_path):
    """Test saving results to a file"""
    # Mock results
    results = {
        "test": "data"
    }
    
    # Save to temporary directory
    output_file = tmp_path / "test_results.json"
    orchestrator.save_results(results, str(output_file))
    
    # Check that file exists and contains correct data
    assert output_file.exists()
    with open(output_file) as f:
        saved_data = f.read()
        assert '"test": "data"' in saved_data 