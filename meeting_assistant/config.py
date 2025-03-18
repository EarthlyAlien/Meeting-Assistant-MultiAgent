from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from pathlib import Path
import os

class AgentConfig(BaseModel):
    """Configuration for individual agents"""
    model_config = ConfigDict(extra='forbid')
    
    openai_api_key: str = Field(..., description="OpenAI API key for GPT models")
    azure_speech_key: str = Field(..., description="Azure Speech Services API key")
    model_name: str = Field("gpt-4", description="GPT model to use")
    temperature: float = Field(0.7, description="Temperature for GPT responses")
    max_tokens: int = Field(1000, description="Maximum tokens for GPT responses")

class WorkspaceConfig(BaseModel):
    """Configuration for workspace and file management"""
    model_config = ConfigDict(extra='forbid')
    
    upload_dir: Path = Field(
        default=Path("uploads"),
        description="Directory for uploaded files"
    )
    results_dir: Path = Field(
        default=Path("results"),
        description="Directory for saving results"
    )
    temp_dir: Path = Field(
        default=Path("temp"),
        description="Directory for temporary files"
    )

class AutoGenConfig(BaseModel):
    """Configuration for AutoGen settings"""
    model_config = ConfigDict(extra='forbid')
    
    use_docker: bool = Field(False, description="Whether to use Docker for code execution")
    max_consecutive_auto_reply: int = Field(
        10,
        description="Maximum number of consecutive auto-replies"
    )
    human_input_mode: str = Field(
        "NEVER",
        description="Mode for human input in conversations"
    )

class AppConfig(BaseModel):
    """Main application configuration"""
    model_config = ConfigDict(extra='forbid')
    
    agent: AgentConfig
    workspace: WorkspaceConfig = WorkspaceConfig()
    autogen: AutoGenConfig = AutoGenConfig()
    debug: bool = Field(False, description="Enable debug mode")
    log_level: str = Field("INFO", description="Logging level")

def load_config() -> AppConfig:
    """Load configuration from environment variables and defaults"""
    agent_config = AgentConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        azure_speech_key=os.getenv("AZURE_SPEECH_KEY", ""),
        model_name=os.getenv("MODEL_NAME", "gpt-4"),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("MAX_TOKENS", "1000"))
    )
    
    return AppConfig(
        agent=agent_config,
        debug=os.getenv("DEBUG", "").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO")
    ) 