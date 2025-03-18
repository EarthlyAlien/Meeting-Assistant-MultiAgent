import os
import tempfile
import pytest
from pathlib import Path
from meeting_assistant import MeetingAssistantOrchestrator

@pytest.fixture
def mock_audio_file():
    """Create a temporary mock audio file for testing"""
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_file.close()
    yield temp_file.name
    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)

@pytest.fixture
def orchestrator(test_config):
    """Create an orchestrator instance for testing"""
    return MeetingAssistantOrchestrator(test_config)

def test_orchestrator_initialization(orchestrator, test_config):
    """Test that the orchestrator initializes correctly"""
    assert orchestrator.config.agent.openai_api_key == "test_openai_key"
    assert orchestrator.config.agent.azure_speech_key == "test_azure_key"
    assert orchestrator.transcription_agent is None
    assert orchestrator.summarization_agent is None
    assert orchestrator.action_item_extraction_agent is None

def test_process_meeting(orchestrator, mock_audio_file, test_dirs):
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
    
    # Check status
    assert results["transcription"]["metadata"]["status"] == "completed"
    assert results["summary"]["metadata"]["status"] == "completed"
    assert results["action_items"]["metadata"]["status"] == "completed"

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

def test_save_results(orchestrator, test_dirs):
    """Test saving results to a file"""
    # Mock results
    results = {
        "test": "data"
    }
    
    # Save to test results directory
    output_file = test_dirs.results_dir / "test_results.json"
    orchestrator.save_results(results, str(output_file))
    
    # Check that file exists and contains correct data
    assert output_file.exists()
    with open(output_file) as f:
        saved_data = f.read()
        assert '"test": "data"' in saved_data

def test_error_handling(orchestrator, test_dirs):
    """Test error handling in various methods"""
    # Test invalid audio file
    with pytest.raises(FileNotFoundError):
        orchestrator.process_meeting("nonexistent_file.wav")
    
    # Test invalid results data
    with pytest.raises(KeyError):
        orchestrator.generate_report({"invalid": "data"})
    
    # Test invalid output directory
    with pytest.raises(ValueError):
        orchestrator.save_results({}, str(Path.cwd() / "invalid" / "path" / "results.json")) 