"""Summarization agent for generating meeting summaries"""


class SummarizationAgent:
    def __init__(self, config):
        self.config = config

    def summarize(self, transcription_result):
        """Mock summarization for testing"""
        return {"summary": "Test summary", "metadata": {"status": "completed"}}
