from fastapi import APIRouter, UploadFile, File, HTTPException

from services.transcription_service import transcription_service

router = APIRouter()


@router.post("/")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe a voice note to text using Whisper."""
    allowed_types = [
        "audio/webm", "audio/mp3", "audio/mpeg",
        "audio/mp4", "audio/m4a", "audio/wav",
        "audio/ogg", "video/webm",
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format: {file.content_type}. Use webm, mp3, m4a, wav, or ogg.",
        )

    audio_bytes = await file.read()
    result = await transcription_service.transcribe_audio(audio_bytes, file.filename or "audio.webm")

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result
