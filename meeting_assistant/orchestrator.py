import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .action_item_extraction_agent import ActionItemExtractionAgent
from .summarization_agent import SummarizationAgent
from .transcription_agent import TranscriptionAgent


class MeetingAssistantOrchestrator:
    """Orchestrates the multi-agent system for processing meetings."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the orchestrator with configuration.

        Args:
            config: Configuration dictionary for the orchestrator and agents.
        """
        self.config = config
        self._setup_agents()
        self._setup_workspace()

    def _setup_agents(self) -> None:
        """Set up the specialized agents for meeting processing."""
        self.transcription_agent = TranscriptionAgent(self.config)
        self.summarization_agent = SummarizationAgent(self.config)
        self.action_item_agent = ActionItemExtractionAgent(self.config)

    def _setup_workspace(self) -> None:
        """Set up the workspace directories."""
        self.output_dir = Path(self.config.get("output_dir", "output"))
        self.temp_dir = Path(self.config.get("temp_dir", "temp"))

        # Create directories if they don't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def process_meeting(self, audio_file: str) -> Dict[str, Any]:
        """Process a meeting recording through the agent pipeline.

        Args:
            audio_file: Path to the meeting audio file.

        Returns:
            Dict containing the processing results from all agents.

        Raises:
            FileNotFoundError: If the audio file doesn't exist.
            ValueError: If the audio file is invalid or processing fails.
        """
        if not Path(audio_file).exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_file}"
            )

        try:
            # Step 1: Transcribe the meeting audio
            transcription_result = self.transcription_agent.transcribe(
                audio_file
            )

            # Step 2: Generate meeting summary
            summary_result = self.summarization_agent.summarize(
                transcription_result
            )

            # Step 3: Extract action items
            action_items = self.action_item_agent.extract_action_items(
                transcription_result,
                summary_result
            )

            # Combine all results
            return {
                "transcription": transcription_result,
                "summary": summary_result,
                "action_items": action_items,
                "metadata": {
                    "audio_file": audio_file,
                    "timestamp": str(datetime.now())
                }
            }

        except Exception as e:
            raise ValueError(
                f"Failed to process meeting: {str(e)}"
            ) from e

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a formatted report from the meeting results.

        Args:
            results: Dictionary containing meeting processing results.

        Returns:
            Formatted report as a string.

        Raises:
            ValueError: If the results data is invalid or incomplete.
        """
        required_fields = {"transcription", "summary", "action_items"}
        if not all(field in results for field in required_fields):
            raise ValueError(
                "Missing required fields in results data"
            )

        report = []
        report.append("# Meeting Summary Report\n")
        report.append(f"Generated: {results['metadata']['timestamp']}\n")
        report.append("\n## Meeting Summary\n")
        report.append(results["summary"])
        report.append("\n## Action Items\n")

        for item in results["action_items"]["action_items"]:
            report.append(
                f"- {item['task']} (Assignee: {item['assignee']}, "
                f"Due: {item['due_date']})"
            )

        return "\n".join(report)

    def save_results(
        self,
        results: Dict[str, Any],
        output_path: str = None
    ) -> str:
        """Save the meeting results to files.

        Args:
            results: Dictionary containing meeting processing results.
            output_path: Optional custom output path.

        Returns:
            Path to the saved report file.

        Raises:
            ValueError: If the results data is invalid or saving fails.
        """
        if not isinstance(results, dict):
            raise ValueError("Results must be a dictionary")

        # Use custom output path or default to output directory
        output_dir = (
            Path(output_path) if output_path
            else self.output_dir
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save the full results as JSON
        results_file = output_dir / f"meeting_results_{timestamp}.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)

        # Generate and save the report
        report = self.generate_report(results)
        report_file = output_dir / f"meeting_report_{timestamp}.md"
        with open(report_file, "w") as f:
            f.write(report)

        return str(report_file)

    def _notify_autogen_agent(self, agent, message: str):
        """Send a message to an AutoGen agent"""
        self.logger.debug(f"Notifying agent {agent.name}: {message}")
        agent.receive({"content": message, "role": "user"})
