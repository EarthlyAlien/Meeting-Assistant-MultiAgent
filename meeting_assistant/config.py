import os
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class AgentConfig(BaseModel):
    """Configuration for individual agents."""

    model_config = ConfigDict(extra="allow")

    api_key: str = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", ""),
        description="API key for the agent",
    )
    model: str = Field(
        default="gpt-4-turbo-preview", description="Model to use for the agent"
    )


class WorkspaceConfig(BaseModel):
    """Configuration for workspace settings."""

    model_config = ConfigDict(extra="allow")

    output_dir: Path = Field(
        default=Path("output"), description="Directory for output files"
    )
    temp_dir: Path = Field(
        default=Path("temp"), description="Directory for temporary files"
    )


class AutoGenConfig(BaseModel):
    """Configuration for AutoGen settings."""

    model_config = ConfigDict(extra="allow")

    use_docker: bool = Field(
        default=False, description="Whether to use Docker for code execution"
    )
    timeout: int = Field(
        default=600, description="Timeout for agent operations in seconds"
    )


class AppConfig(BaseModel):
    """Main application configuration."""

    model_config = ConfigDict(extra="allow")

    agents: AgentConfig = Field(
        default_factory=AgentConfig, description="Agent-specific configuration"
    )
    workspace: WorkspaceConfig = Field(
        default_factory=WorkspaceConfig, description="Workspace settings"
    )
    autogen: AutoGenConfig = Field(
        default_factory=AutoGenConfig, description="AutoGen configuration"
    )


def load_config() -> AppConfig:
    """Load configuration from environment variables and defaults.

    Returns:
        AppConfig: The loaded configuration object.
    """
    return AppConfig()
