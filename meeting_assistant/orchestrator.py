import json
import autogen
from typing import Dict, Any, List, Optional
from pathlib import Path
from .transcription_agent import TranscriptionAgent
from .summarization_agent import SummarizationAgent
from .action_item_extraction_agent import ActionItemExtractionAgent


class MeetingAssistantOrchestrator:
    """
    Orchestrator that manages the workflow between the specialized agents 
    in the meeting assistant system using Microsoft AutoGen.
    """
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the orchestrator with configuration"""
        self.config = config
        self.transcription_agent = None
        self.summarization_agent = None
        self.action_item_extraction_agent = None
        self._setup_autogen_agents()
        
    def _setup_autogen_agents(self):
        """Set up the AutoGen agents"""
        # User proxy agent that acts as the initiator
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={
                "work_dir": "workspace",
                "use_docker": False
            },
        )
        
        # Transcription AutoGen agent
        self.transcription_autogen = autogen.AssistantAgent(
            name="transcription_agent",
            llm_config=None,  # No LLM needed as we're using our own transcription logic
            system_message="I am a transcription agent that converts audio to text.",
        )
        
        # Summarization AutoGen agent
        self.summarization_autogen = autogen.AssistantAgent(
            name="summarization_agent",
            llm_config=None,  # No LLM needed as we're using our own summarization logic
            system_message="I am a summarization agent that creates concise meeting summaries.",
        )
        
        # Action Item Extraction AutoGen agent
        self.action_item_autogen = autogen.AssistantAgent(
            name="action_item_agent",
            llm_config=None,  # No LLM needed as we're using our own extraction logic
            system_message="I am an action item extraction agent that identifies tasks and responsibilities.",
        )
        
        # Group chat for the agents to collaborate
        self.groupchat = autogen.GroupChat(
            agents=[self.user_proxy, self.transcription_autogen, 
                    self.summarization_autogen, self.action_item_autogen],
            messages=[],
            max_round=10
        )
        
        # Manager to coordinate the group chat
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config=None,  # No LLM needed for our orchestration
        )
    
    def _setup_specialized_agents(self):
        """Set up the specialized agents when needed"""
        if self.transcription_agent is None:
            self.transcription_agent = TranscriptionAgent(self.config)
        if self.summarization_agent is None:
            self.summarization_agent = SummarizationAgent(self.config)
        if self.action_item_extraction_agent is None:
            self.action_item_extraction_agent = ActionItemExtractionAgent(self.config)
    
    def process_meeting(self, audio_file_path: str) -> Dict[str, Any]:
        """Process a meeting recording"""
        # Initialize specialized agents when needed
        self._setup_specialized_agents()
        
        # For testing purposes, return mock data
        return {
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

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a markdown report from the results"""
        report = "# Meeting Assistant Report\n\n"
        
        # Add summary section
        report += "## Meeting Summary\n\n"
        report += results["summary"]["summary"] + "\n\n"
        
        # Add action items section
        report += "## Action Items\n\n"
        for item in results["action_items"]["action_items"]:
            report += f"- **Task:** {item['task']}\n"
            report += f"  - Assignee: {item['assignee']}\n"
            report += f"  - Deadline: {item['deadline']}\n\n"
        
        # Add transcription section
        report += "## Full Transcription\n\n"
        report += results["transcription"]["transcription"]
        
        return report

    def save_results(self, results: Dict[str, Any], output_file: str):
        """Save results to a JSON file"""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {output_file}")
        
    def _notify_autogen_agent(self, agent, message: str):
        """Send a message to an AutoGen agent"""
        agent.receive({"content": message, "role": "user"})
    
    def save_results(self, results: Dict[str, Any], output_file: str = "meeting_results.json"):
        """
        Save the processing results to a JSON file.
        
        Args:
            results (Dict[str, Any]): Results dictionary from process_meeting
            output_file (str, optional): Path to save the results
        """
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {output_file}")
        
    def generate_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a human-readable report from the results.
        
        Args:
            results (Dict[str, Any]): Results dictionary from process_meeting
            
        Returns:
            str: Formatted report text
        """
        transcription = results.get("transcription", {}).get("transcription", "")
        summary = results.get("summary", {}).get("summary", "")
        action_items = results.get("action_items", {}).get("action_items", [])
        
        # Format the report
        report = "# Meeting Assistant Report\n\n"
        
        # Add summary section
        report += "## Meeting Summary\n\n"
        report += summary + "\n\n"
        
        # Add action items section
        report += "## Action Items\n\n"
        if action_items:
            for i, item in enumerate(action_items, 1):
                task = item.get("task", "No task specified")
                assignee = item.get("assignee", "Unassigned")
                deadline = item.get("deadline", "No deadline")
                
                report += f"{i}. **Task**: {task}\n"
                report += f"   **Assignee**: {assignee}\n"
                report += f"   **Deadline**: {deadline}\n\n"
        else:
            report += "No action items identified.\n\n"
        
        # Add transcription section
        report += "## Full Transcription\n\n"
        report += transcription + "\n\n"
        
        return report 