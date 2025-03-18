import json
import os
import tempfile

from orchestrator import MeetingAssistantOrchestrator


def create_mock_audio_file():
    """
    Create a temporary mock audio file for demonstration purposes.
    In a real scenario, you would use an actual audio file.

    Returns:
        str: Path to the temporary file
    """
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_file.close()

    print(f"Created mock audio file at: {temp_file.name}")

    return temp_file.name


def mock_transcription_process(orchestrator, audio_file_path):
    """
    Mock the transcription process with predefined text.

    Args:
        orchestrator: MeetingAssistantOrchestrator instance
        audio_file_path: Path to the audio file (not actually used)

    Returns:
        dict: Results with mock transcription, summary, and action items
    """
    # Store the original transcribe method
    original_transcribe = orchestrator.transcription_agent.transcribe

    # Mock transcription data
    mock_transcript = """
    John: Good morning everyone. Let's start our weekly project meeting. First, let's review the progress from last week.
    
    Sarah: I've completed the design phase for the new user interface. We need to review it together by Friday.
    
    Michael: Great job, Sarah. I'll work on the backend integration and will need at least a week to complete it.
    
    John: Perfect. David, can you update us on the testing framework?
    
    David: Sure, I've set up the initial framework but I need to finalize the test cases. I'll finish that by next Monday.
    
    John: That sounds good. Let's also discuss the upcoming client presentation. We have to prepare slides by the end of this month.
    
    Sarah: I'll take care of the UI/UX portion of the slides. Michael, can you handle the technical architecture section?
    
    Michael: Yes, I'll prepare that by Wednesday next week.
    
    John: Excellent. David, please make sure to include some testing metrics in the presentation.
    
    David: Noted, I'll have those ready along with my test cases.
    
    John: Great. As a reminder, our deployment deadline is August 15th. We need to ensure everything is ready by then.
    
    Sarah: Should we schedule a pre-launch meeting in the first week of August?
    
    John: Good idea. Let's schedule it for August 3rd. Everyone, please mark your calendars.
    
    Michael: One more thing - we need to coordinate with the marketing team about the launch announcement.
    
    John: You're right. I'll set up a meeting with them next week. Any other points we need to discuss?
    
    David: Just a heads-up that I'll be on vacation the last week of July.
    
    John: Thanks for letting us know, David. Please make sure your tasks are covered.
    
    David: Already arranged that with the junior testers. They're up to speed.
    
    John: Perfect. If there's nothing else, we can wrap up. Thanks everyone for your updates.
    """

    # Replace the transcribe method with a mock function
    def mock_transcribe(audio_file_path):
        return {
            "transcription": mock_transcript,
            "metadata": {
                "file": audio_file_path,
                "duration_seconds": 720,  # 12 minutes
                "status": "completed",
            },
        }

    # Set the mock function
    orchestrator.transcription_agent.transcribe = mock_transcribe

    try:
        # Process the meeting with mock data
        results = orchestrator.process_meeting(audio_file_path)
        return results
    finally:
        # Restore the original function
        orchestrator.transcription_agent.transcribe = original_transcribe


def run_sample():
    """Run a sample demonstration of the Meeting Assistant"""
    # Create a mock audio file
    audio_file_path = create_mock_audio_file()

    try:
        # Configure the orchestrator
        config = {
            "openai_api_key": os.environ.get("OPENAI_API_KEY"),
            "azure_speech_key": os.environ.get("AZURE_SPEECH_KEY"),
        }

        # Create the orchestrator
        orchestrator = MeetingAssistantOrchestrator(config)

        print("Running Meeting Assistant with mock data...")

        # Process the meeting with mock transcription
        results = mock_transcription_process(orchestrator, audio_file_path)

        # Save results
        orchestrator.save_results(results, "sample_results.json")

        # Generate and save a report
        report = orchestrator.generate_report(results)
        with open("sample_report.md", "w") as f:
            f.write(report)

        print("\nSample completed successfully!")
        print("- Results saved to: sample_results.json")
        print("- Report saved to: sample_report.md")

        # Print action items
        action_items = results["action_items"].get("action_items", [])
        if action_items:
            print("\nExtracted Action Items:")
            for i, item in enumerate(action_items, 1):
                task = item.get("task", "No task specified")
                assignee = item.get("assignee", "Unassigned")
                deadline = item.get("deadline", "No deadline")

                print(f"  {i}. Task: {task}")
                print(f"     Assignee: {assignee}")
                print(f"     Deadline: {deadline}")

    finally:
        # Clean up the temporary file
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
            print(f"Cleaned up mock audio file: {audio_file_path}")


if __name__ == "__main__":
    run_sample()
