import json
import re
import openai


class ActionItemExtractionAgent:
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        # Regular expressions for simple action item extraction
        self.action_keywords = [
            r'(?:need to|must|should|will|going to|have to|shall) ([^.!?]*)',
            r'(?:action item|task|todo|to-do|to do|follow-up|followup)[:\s]* ([^.!?]*)',
            r'(\w+)(?:\s*will|\s*is going to|\s*needs to|\s*must) ([^.!?]*)',
            r'(?:by|before|due)(?:\s*the)?\s*(\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)|tomorrow|next week|(?:this|next) month|(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))',
        ]
    
    def extract_action_items(self, transcription, summary=None):
        """
        Extract action items from meeting transcription and/or summary.
        
        Args:
            transcription (dict): Transcription data from the TranscriptionAgent
            summary (dict, optional): Summary data from the SummarizationAgent
            
        Returns:
            dict: Extraction result with list of action items and metadata
        """
        print("ActionItemExtractionAgent: Extracting action items")
        
        try:
            # Use both transcription and summary if available
            text = transcription.get("transcription", "")
            
            if summary and "summary" in summary:
                text += "\n\n" + summary["summary"]
            
            if not text:
                raise ValueError("No text provided for action item extraction")
            
            # Extract action items using provided method
            action_items = self._extract_action_items(text)
            
            return {
                "action_items": action_items,
                "metadata": {
                    "items_found": len(action_items),
                    "status": "completed"
                }
            }
            
        except Exception as e:
            print(f"Error during action item extraction: {str(e)}")
            return {
                "action_items": [],
                "metadata": {
                    "status": "error",
                    "error": str(e)
                }
            }
    
    def _extract_action_items(self, text):
        """
        Extract action items from the provided text.
        
        This is a placeholder method. In a production environment, 
        this would use more sophisticated NLP techniques or an LLM.
        """
        # If API key is provided, use LLM for extraction
        if self.api_key:
            try:
                return self._extract_with_llm(text)
            except Exception as e:
                print(f"Error with LLM extraction: {str(e)}")
                return self._extract_with_regex(text)
        else:
            # Fallback to regex-based extraction
            return self._extract_with_regex(text)
    
    def _extract_with_llm(self, text):
        """Extract action items using an LLM"""
        client = openai.OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a meeting assistant that extracts action items from meeting transcripts. Extract all tasks, responsibilities, and deadlines in a structured format."},
                {"role": "user", "content": f"Extract all action items from this meeting transcript as a JSON array. Each action item should have 'task', 'assignee', and 'deadline' fields. Use null for missing information:\n\n{text}"}
            ],
            response_format={"type": "json_object"},
            max_tokens=1000
        )
        
        # Parse the response
        result_content = response.choices[0].message.content
        try:
            result_json = json.loads(result_content)
            return result_json.get("action_items", [])
        except:
            # If parsing fails, return an empty list
            return []
    
    def _extract_with_regex(self, text):
        """Extract action items using regular expressions"""
        action_items = []
        sentences = re.split(r'[.!?]\s+', text)
        
        for sentence in sentences:
            item = self._extract_from_sentence(sentence)
            if item and all(item != existing for existing in action_items):
                action_items.append(item)
        
        return action_items
    
    def _extract_from_sentence(self, sentence):
        """Extract an action item from a single sentence using pattern matching"""
        sentence = sentence.strip()
        if not sentence:
            return None
        
        # Look for action patterns
        task = None
        assignee = None
        deadline = None
        
        # Find potential task
        for pattern in self.action_keywords:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                task = match.group(1).strip()
                break
        
        if not task:
            return None
        
        # Try to find assignee - look for names followed by verbs
        assignee_match = re.search(r'(\b[A-Z][a-z]+\b)(?:\s+will|\s+should|\s+is going to|\s+needs to)', sentence)
        if assignee_match:
            assignee = assignee_match.group(1)
        
        # Try to find deadline
        deadline_pattern = r'(?:by|before|due)(?:\s*the)?\s*(\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)|tomorrow|next week|(?:this|next) month|(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))'
        deadline_match = re.search(deadline_pattern, sentence, re.IGNORECASE)
        if deadline_match:
            deadline = deadline_match.group(1)
        
        return {
            "task": task,
            "assignee": assignee,
            "deadline": deadline
        } 