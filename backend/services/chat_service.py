from openai import OpenAI
from core.config import settings
from sqlalchemy.orm import Session
from models.conversation import ChatMessage, ChatSession, ContactMemory
import json
import base64

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are RIZZA — an expert AI relationship and messaging strategist. You help people navigate their conversations, relationships, and social dynamics.

Your personality:
- Warm, witty, and insightful
- You give practical, actionable advice
- You read between the lines of conversations
- You understand emotional dynamics and communication patterns
- You never judge — you strategize

When the user shares a screenshot of a conversation, analyze it deeply:
- Extract who said what
- Read the emotional undertones
- Identify communication patterns
- Suggest strategic replies with different tones

When you learn something about a contact the user mentions (name, personality traits, communication style, relationship dynamics), remember it for future conversations.

Always respond in a conversational, friendly tone. You're like a smart best friend who happens to be an expert in communication psychology.

If the user asks for reply suggestions, provide 2-3 options with different tones (warm, playful, direct) and explain the strategy behind each."""


class ChatService:
    def __init__(self):
        self.model = "gpt-4o"
        self.text_model = "gpt-4o-mini"

    def _get_or_create_session(self, db: Session) -> ChatSession:
        """Get the most recent session or create a new one."""
        session = db.query(ChatSession).order_by(ChatSession.updated_at.desc()).first()
        if not session:
            session = ChatSession()
            db.add(session)
            db.commit()
            db.refresh(session)
        return session

    def _get_memory_context(self, db: Session) -> str:
        """Load all contact memories into a context string."""
        memories = db.query(ContactMemory).all()
        if not memories:
            return ""
        
        memory_lines = []
        contacts = {}
        for m in memories:
            if m.contact_name not in contacts:
                contacts[m.contact_name] = []
            contacts[m.contact_name].append(m.fact)
        
        for name, facts in contacts.items():
            memory_lines.append(f"\n{name}:")
            for fact in facts:
                memory_lines.append(f"  - {fact}")
        
        return "\n\n[CONTACT MEMORIES — things you remember about people the user has discussed:]\n" + "\n".join(memory_lines)

    def _build_messages(self, db: Session, chat_session: ChatSession, new_content: str, image_bytes: bytes | None = None):
        """Build the OpenAI messages array from history + new message."""
        memory_context = self._get_memory_context(db)
        system_content = SYSTEM_PROMPT
        if memory_context:
            system_content += memory_context

        messages = [{"role": "system", "content": system_content}]

        # Add history (last 20 messages for context window management)
        history = db.query(ChatMessage).filter(
            ChatMessage.session_id == chat_session.id
        ).order_by(ChatMessage.created_at).all()
        
        recent_history = history[-20:] if len(history) > 20 else history
        
        for msg in recent_history:
            messages.append({"role": msg.role, "content": msg.content})

        # Build the new user message
        if image_bytes:
            base64_image = base64.b64encode(image_bytes).decode("utf-8")
            content_parts = []
            if new_content:
                content_parts.append({"type": "text", "text": new_content})
            content_parts.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
            })
            messages.append({"role": "user", "content": content_parts})
        else:
            messages.append({"role": "user", "content": new_content})

        return messages

    async def send_message(self, db: Session, content: str, image_bytes: bytes | None = None) -> dict:
        """Send a message and get AI response."""
        try:
            chat_session = self._get_or_create_session(db)
            
            # Build messages for OpenAI
            messages = self._build_messages(db, chat_session, content, image_bytes)
            
            # Choose model based on whether there's an image
            model = self.model if image_bytes else self.text_model

            # Call OpenAI
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1024,
            )

            assistant_text = response.choices[0].message.content

            # Save user message
            user_msg = ChatMessage(
                session_id=chat_session.id,
                role="user",
                content=content or "[Sent an image]",
                image_path=None,
                is_voice=False,
            )
            db.add(user_msg)

            # Save assistant message
            assistant_msg = ChatMessage(
                session_id=chat_session.id,
                role="assistant",
                content=assistant_text,
            )
            db.add(assistant_msg)
            db.commit()

            # Try to extract contact memories in background
            await self._extract_memories(db, content, assistant_text)

            return {
                "response": assistant_text,
                "session_id": chat_session.id,
            }

        except Exception as e:
            print(f"Chat error: {e}")
            return {"error": str(e)}

    async def _extract_memories(self, db: Session, user_message: str, ai_response: str):
        """Auto-extract contact facts from the conversation."""
        try:
            extraction_prompt = f"""From this conversation exchange, extract any new facts about specific people (contacts) being discussed. 
Only extract if there are concrete, memorable facts about a named person.

User said: {user_message}
AI responded: {ai_response}

If there are facts to extract, return JSON:
{{"memories": [{{"contact_name": "...", "fact": "...", "category": "personality|pattern|preference|history"}}]}}

If there's nothing to extract, return:
{{"memories": []}}"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": extraction_prompt}],
                response_format={"type": "json_object"},
                max_tokens=300,
            )

            result = json.loads(response.choices[0].message.content)
            
            for memory in result.get("memories", []):
                existing = db.query(ContactMemory).filter(
                    ContactMemory.contact_name == memory["contact_name"],
                    ContactMemory.fact == memory["fact"],
                ).first()
                
                if not existing:
                    new_memory = ContactMemory(
                        contact_name=memory["contact_name"],
                        fact=memory["fact"],
                        category=memory.get("category", "general"),
                    )
                    db.add(new_memory)
            
            db.commit()
        except Exception as e:
            print(f"Memory extraction error (non-critical): {e}")

    def get_history(self, db: Session) -> list:
        """Get chat history."""
        chat_session = db.query(ChatSession).order_by(ChatSession.updated_at.desc()).first()
        if not chat_session:
            return []
        
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == chat_session.id
        ).order_by(ChatMessage.created_at).all()

        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "is_voice": msg.is_voice,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in messages
        ]

    def clear_history(self, db: Session):
        """Clear all chat history (start fresh)."""
        db.query(ChatMessage).delete()
        db.query(ChatSession).delete()
        db.commit()


chat_service = ChatService()
