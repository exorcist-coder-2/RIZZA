from openai import OpenAI
from core.config import settings
from PIL import Image
import io
import base64

# Configure OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class VisionService:
    def __init__(self):
        self.model = "gpt-4o"

    async def analyze_chat_screenshot(self, image_bytes: bytes) -> dict:
        """
        Analyzes a chat screenshot to extract conversation, emotion, and tone.
        """
        try:
            # Convert image bytes to base64
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            prompt = """
            Analyze this chat screenshot. Extract the following in JSON format:
            1. "conversation": A list of message objects with "sender" (string, use 'User' or 'Partner'), "text" (string), and "emotion" (string, e.g., happy, angry, neutral).
            2. "summary": A brief summary of the conversation context.
            3. "overall_mood": The overall emotional tone of the conversation (e.g., Flirty, Tense, Casual).
            4. "participant_name": The name of the other person if visible, else "Partner".
            
            Ensure the JSON is raw and valid.
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return {"error": str(e)}

vision_service = VisionService()
