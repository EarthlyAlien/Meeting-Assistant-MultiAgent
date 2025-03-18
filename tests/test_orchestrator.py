import os
import tempfile
from pathlib import Path

import pytest

from meeting_assistant import MeetingAssistantOrchestrator


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
    """Test that the orchestrator is initialized correctly."""
    assert orchestrator is not None
    assert orchestrator.config is not None
    assert orchestrator.transcription_agent is not None
    assert orchestrator.summarization_agent is not None
    assert orchestrator.action_item_agent is not None


def test_process_meeting(orchestrator, tmp_path):
    """Test processing a meeting recording."""
    # Create a temporary audio file
    audio_file = tmp_path / "test.wav"
    audio_file.write_bytes(b"dummy audio data")

    # Process the meeting
    results = orchestrator.process_meeting(str(audio_file))

    # Verify the results structure
    assert "transcription" in results
    assert "summary" in results
    assert "action_items" in results
    assert "metadata" in results
    assert results["metadata"]["audio_file"] == str(audio_file)


def test_generate_report(orchestrator, sample_results):
    """Test generating a report from meeting results."""
    report = orchestrator.generate_report(sample_results)

    # Verify report content
    assert "Meeting Summary Report" in report
    assert "Generated:" in report
    assert "Meeting Summary" in report
    assert "Action Items" in report
    assert "Test task" in report
    assert "John" in report
    assert "2024-03-15" in report


def test_save_results(orchestrator, sample_results, tmp_path):
    """Test saving meeting results to files."""
    # Save results to temporary directory
    report_path = orchestrator.save_results(
        sample_results,
        str(tmp_path)
    )

    # Verify files were created
    assert len(list(tmp_path.glob("meeting_results_*.json"))) == 1
    assert len(list(tmp_path.glob("meeting_report_*.md"))) == 1

    # Verify report file path
    assert Path(report_path).exists()


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
        orchestrator.save_results(
            {}, str(Path.cwd() / "invalid" / "path" / "results.json")
        )
