"""Transcription agent for converting audio to text"""


class TranscriptionAgent:
    def __init__(self, config):
        self.config = config

    def transcribe(self, audio_file_path):
        """Mock transcription for testing"""
        return {
            "transcription": "Test transcription",
            "metadata": {"status": "completed"},
        }
