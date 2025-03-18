import json
import autogen
from typing import Dict, Any, List, Optional
from transcription_agent import TranscriptionAgent
from summarization_agent import SummarizationAgent
from action_item_extraction_agent import ActionItemExtractionAgent


class MeetingAssistantOrchestrator:
    """
    Orchestrator that manages the workflow between the specialized agents 
    in the meeting assistant system using Microsoft AutoGen.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the orchestrator with configuration.
        
        Args:
            config (Dict[str, Any], optional): Configuration dictionary with API keys and settings
        """
        self.config = config or {}
        self._setup_agents()
        
    def _setup_agents(self):
        """Set up the specialized agents and AutoGen agents"""
        # Initialize the specialized agents
        self.transcription_agent = TranscriptionAgent(
            api_key=self.config.get("azure_speech_key")
        )
        
        self.summarization_agent = SummarizationAgent(
            api_key=self.config.get("openai_api_key"),
            model=self.config.get("summarization_model", "gpt-3.5-turbo")
        )
        
        self.action_item_extraction_agent = ActionItemExtractionAgent(
            api_key=self.config.get("openai_api_key"),
            model=self.config.get("extraction_model", "gpt-3.5-turbo")
        )
        
        # Set up the AutoGen agents
        # User proxy agent that acts as the initiator
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"work_dir": "workspace"},
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
    
    def process_meeting(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Process a meeting recording through the entire pipeline.
        
        Args:
            audio_file_path (str): Path to the audio file of the meeting
            
        Returns:
            Dict[str, Any]: Results dictionary with transcription, summary, and action items
        """
        # Step 1: Transcribe the audio
        transcription_result = self.transcription_agent.transcribe(audio_file_path)
        
        # Log the result and inform AutoGen agents
        print(f"Transcription completed: {len(transcription_result.get('transcription', ''))} characters")
        self._notify_autogen_agent(
            self.transcription_autogen, 
            f"Transcription completed for {audio_file_path}. Result: {json.dumps(transcription_result, indent=2)}"
        )
        
        # Step 2: Generate summary
        summary_result = self.summarization_agent.summarize(transcription_result)
        
        # Log the result and inform AutoGen agents
        print(f"Summary generated: {len(summary_result.get('summary', ''))} characters")
        self._notify_autogen_agent(
            self.summarization_autogen, 
            f"Summary generated from transcription. Result: {json.dumps(summary_result, indent=2)}"
        )
        
        # Step 3: Extract action items
        action_items_result = self.action_item_extraction_agent.extract_action_items(
            transcription_result, 
            summary_result
        )
        
        # Log the result and inform AutoGen agents
        print(f"Action items extracted: {len(action_items_result.get('action_items', []))} items")
        self._notify_autogen_agent(
            self.action_item_autogen, 
            f"Action items extracted from meeting content. Result: {json.dumps(action_items_result, indent=2)}"
        )
        
        # Terminate the group chat
        self._notify_autogen_agent(
            self.user_proxy,
            "All tasks completed. TERMINATE"
        )
        
        # Return the combined results
        return {
            "transcription": transcription_result,
            "summary": summary_result,
            "action_items": action_items_result
        }
    
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