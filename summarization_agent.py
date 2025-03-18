import json
import openai


class SummarizationAgent:
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
    
    def summarize(self, transcription):
        """
        Generate a concise summary of the meeting transcription.
        
        Args:
            transcription (dict): Transcription data from the TranscriptionAgent
            
        Returns:
            dict: Summary result with summarized text and metadata
        """
        print("SummarizationAgent: Generating meeting summary")
        
        try:
            # Extract the transcription text
            text = transcription.get("transcription", "")
            
            if not text:
                raise ValueError("No transcription text provided")
            
            # For demonstration purposes, we'll use a placeholder summary generator
            # In production, this would use the OpenAI API or similar service
            summary = self._generate_summary(text)
            
            return {
                "summary": summary,
                "metadata": {
                    "original_length": len(text),
                    "summary_length": len(summary),
                    "status": "completed"
                }
            }
            
        except Exception as e:
            print(f"Error during summarization: {str(e)}")
            return {
                "summary": "",
                "metadata": {
                    "status": "error",
                    "error": str(e)
                }
            }
    
    def _generate_summary(self, text):
        """
        Generate a summary of the provided text.
        
        This is a placeholder method. In a production environment, 
        this would call an LLM API like OpenAI's GPT models.
        """
        # Placeholder implementation - in production, use OpenAI API or similar
        if self.api_key:
            try:
                # Initialize OpenAI client with the API key
                client = openai.OpenAI(api_key=self.api_key)
                
                # Call the OpenAI API to generate a summary
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a meeting assistant that creates concise summaries."},
                        {"role": "user", "content": f"Please summarize this meeting transcript:\n\n{text}"}
                    ],
                    max_tokens=500
                )
                
                # Extract the summary from the response
                summary = response.choices[0].message.content
                return summary
                
            except Exception as e:
                print(f"Error with OpenAI API: {str(e)}")
                return self._fallback_summary(text)
        else:
            return self._fallback_summary(text)
    
    def _fallback_summary(self, text):
        """Fallback method to generate a simple summary when API is not available"""
        # Simple extractive summary - take the first few sentences as a summary
        sentences = text.split('. ')
        num_summary_sentences = min(5, len(sentences))
        summary = '. '.join(sentences[:num_summary_sentences])
        
        if summary and not summary.endswith('.'):
            summary += '.'
            
        return summary 