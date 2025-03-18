import os
import tempfile
from pathlib import Path

import pytest

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
def orchestrator(test_config):
    """Create an orchestrator instance for testing"""
    return MeetingAssistantOrchestrator(test_config)


def test_orchestrator_initialization(orchestrator):
    """Test that the orchestrator initializes correctly"""
    assert isinstance(orchestrator, MeetingAssistantOrchestrator)
    assert orchestrator.output_dir.exists()
    assert orchestrator.temp_dir.exists()


def test_process_meeting(orchestrator, mock_audio_file):
    """Test processing a meeting recording"""
    results = orchestrator.process_meeting(mock_audio_file)
    assert "transcription" in results
    assert "summary" in results
    assert "action_items" in results
    assert "metadata" in results
    assert results["metadata"]["audio_file"] == mock_audio_file


def test_generate_report(orchestrator, sample_results):
    """Test generating a report from meeting results"""
    report = orchestrator.generate_report(sample_results)
    assert "Meeting Summary Report" in report
    assert "Sample meeting summary" in report
    assert "Test task" in report
    assert "John" in report


def test_save_results(orchestrator, sample_results, tmp_path):
    """Test saving meeting results to files"""
    report_path = orchestrator.save_results(sample_results, str(tmp_path))
    assert Path(report_path).exists()
    assert (tmp_path / "meeting_results_").parent.exists()


def test_error_handling(orchestrator):
    """Test error handling for invalid inputs"""
    with pytest.raises(FileNotFoundError):
        orchestrator.process_meeting("nonexistent.wav")

    with pytest.raises(ValueError):
        orchestrator.generate_report({"invalid": "data"})

    with pytest.raises(ValueError):
        orchestrator.save_results("not a dict")
