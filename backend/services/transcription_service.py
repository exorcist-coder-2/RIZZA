from openai import OpenAI
from core.config import settings
import tempfile
import os

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class TranscriptionService:
    def __init__(self):
        self.model = "whisper-1"

    async def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.webm") -> dict:
        """Transcribe audio bytes using OpenAI Whisper."""
        try:
            # Determine file extension from filename
            ext = os.path.splitext(filename)[1] or ".webm"
            
            # Write to temp file (Whisper API needs a file)
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name

            try:
                with open(tmp_path, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model=self.model,
                        file=audio_file,
                    )
                return {"text": transcript.text}
            finally:
                os.unlink(tmp_path)

        except Exception as e:
            print(f"Transcription error: {e}")
            return {"error": str(e)}


transcription_service = TranscriptionService()
