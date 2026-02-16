from openai import OpenAI
from core.config import settings
import json

# Configure OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class LLMService:
    def __init__(self):
        self.model = "gpt-4o-mini"

    async def generate_replies(self, conversation_context: dict) -> dict:
        """
        Generates 3-tone replies based on conversation context.
        """
        try:
            prompt = f"""
            You are an expert relationship strategist.
            
            Context:
            {json.dumps(conversation_context, indent=2)}
            
            Task:
            Generate 3 distinct reply options for the USER to send back.
            1. Warm / Supportive
            2. Playful / Light
            3. Direct / Confident
            
            Output JSON format:
            {{
                "replies": [
                    {{ "tone": "Warm & Supportive", "text": "...", "reasoning": "..." }},
                    {{ "tone": "Playful & Light", "text": "...", "reasoning": "..." }},
                    {{ "tone": "Direct & Confident", "text": "...", "reasoning": "..." }}
                ]
            }}
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating replies: {e}")
            return {"error": str(e)}

llm_service = LLMService()
