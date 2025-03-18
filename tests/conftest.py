import os
import tempfile
import pytest
from pathlib import Path
from meeting_assistant.config import AppConfig, AgentConfig, WorkspaceConfig, AutoGenConfig

@pytest.fixture
def mock_audio_file():
    """Create a temporary mock audio file for testing"""
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
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
        max_tokens=1000
    )
    
    workspace_config = WorkspaceConfig(
        upload_dir=Path("test_uploads"),
        results_dir=Path("test_results"),
        temp_dir=Path("test_temp")
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
        log_level="DEBUG"
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
    import shutil
    for dir_path in [
        test_config.workspace.upload_dir,
        test_config.workspace.results_dir,
        test_config.workspace.temp_dir
    ]:
        if dir_path.exists():
            shutil.rmtree(dir_path) 