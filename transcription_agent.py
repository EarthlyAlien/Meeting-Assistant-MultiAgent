import json
import os
import tempfile

import speech_recognition as sr
from pydub import AudioSegment


class TranscriptionAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_file_path):
        """
        Transcribe audio file to text using speech recognition.

        Args:
            audio_file_path (str): Path to the audio file

        Returns:
            dict: Transcription result with text and metadata
        """
        print(f"TranscriptionAgent: Transcribing file {audio_file_path}")

        # For prototype, use a simple transcription method
        # In production, this would use Azure Speech-to-Text or similar service
        try:
            # Handle different audio formats - convert to wav if needed
            audio_format = audio_file_path.split(".")[-1].lower()
            if audio_format != "wav":
                temp_wav = self._convert_to_wav(audio_file_path)
                audio_path = temp_wav
            else:
                audio_path = audio_file_path

            # Perform the transcription
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(
                    audio_data
                )  # Placeholder for Azure service

            # Clean up temp file if one was created
            if audio_format != "wav":
                os.remove(temp_wav)

            # Return the transcription result
            result = {
                "transcription": text,
                "metadata": {
                    "file": audio_file_path,
                    "duration_seconds": self._get_audio_duration(audio_file_path),
                    "status": "completed",
                },
            }

            return result

        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            return {
                "transcription": "",
                "metadata": {
                    "file": audio_file_path,
                    "status": "error",
                    "error": str(e),
                },
            }

    def _convert_to_wav(self, audio_file_path):
        """Convert audio file to WAV format for processing"""
        audio = AudioSegment.from_file(audio_file_path)
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        audio.export(temp_file.name, format="wav")
        return temp_file.name

    def _get_audio_duration(self, audio_file_path):
        """Get duration of audio file in seconds"""
        audio = AudioSegment.from_file(audio_file_path)
        return len(audio) / 1000  # Convert milliseconds to seconds
