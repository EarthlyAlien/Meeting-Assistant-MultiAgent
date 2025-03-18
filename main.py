import os
import argparse
from orchestrator import MeetingAssistantOrchestrator


def main():
    """
    Main function to demonstrate the Meeting Assistant workflow.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Intelligent Meeting Assistant')
    parser.add_argument('--audio', type=str, required=True, help='Path to the meeting audio file')
    parser.add_argument('--openai_api_key', type=str, help='OpenAI API key for summarization and extraction')
    parser.add_argument('--azure_speech_key', type=str, help='Azure Speech API key for transcription')
    parser.add_argument('--output', type=str, default='meeting_results.json', help='Output JSON file path')
    parser.add_argument('--report', type=str, default='meeting_report.md', help='Output report file path')
    
    args = parser.parse_args()
    
    # Check if the audio file exists
    if not os.path.isfile(args.audio):
        print(f"Error: Audio file '{args.audio}' not found.")
        return
    
    # Get API keys from environment variables if not provided
    openai_api_key = args.openai_api_key or os.environ.get('OPENAI_API_KEY')
    azure_speech_key = args.azure_speech_key or os.environ.get('AZURE_SPEECH_KEY')
    
    # Configure the orchestrator
    config = {
        "openai_api_key": openai_api_key,
        "azure_speech_key": azure_speech_key,
        "summarization_model": "gpt-3.5-turbo",
        "extraction_model": "gpt-3.5-turbo"
    }
    
    # Create and run the orchestrator
    orchestrator = MeetingAssistantOrchestrator(config)
    
    print(f"Processing meeting audio: {args.audio}")
    
    # Process the meeting
    results = orchestrator.process_meeting(args.audio)
    
    # Save results to JSON
    orchestrator.save_results(results, args.output)
    
    # Generate and save a human-readable report
    report = orchestrator.generate_report(results)
    with open(args.report, 'w') as f:
        f.write(report)
    
    print(f"Report saved to {args.report}")
    
    # Print a summary to the console
    print("\nMeeting Processing Summary:")
    print(f"- Audio file: {args.audio}")
    print(f"- Transcription: {len(results['transcription'].get('transcription', ''))} characters")
    print(f"- Summary: {len(results['summary'].get('summary', ''))} characters")
    print(f"- Action items: {len(results['action_items'].get('action_items', []))} items")
    
    # Print the action items
    action_items = results['action_items'].get('action_items', [])
    if action_items:
        print("\nAction Items:")
        for i, item in enumerate(action_items, 1):
            task = item.get('task', 'No task specified')
            assignee = item.get('assignee', 'Unassigned')
            deadline = item.get('deadline', 'No deadline')
            
            print(f"  {i}. Task: {task}")
            print(f"     Assignee: {assignee}")
            print(f"     Deadline: {deadline}")
    

if __name__ == "__main__":
    main() 