const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface ChatMessage {
    id: number;
    role: 'user' | 'assistant';
    content: string;
    is_voice?: boolean;
    created_at: string;
}

export interface ChatResponse {
    response: string;
    session_id: number;
}

export interface TranscriptionResponse {
    text: string;
}

export interface AnalysisResult {
    conversation: Array<{ sender: string; text: string; emotion: string }>;
    summary: string;
    overall_mood: string;
    participant_name: string;
    replies: Array<{ tone: string; text: string; reasoning: string }>;
}

export async function analyzeScreenshot(file: File): Promise<AnalysisResult> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/analyze/`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to analyze screenshot');
    }

    return response.json();
}

/**
 * Send a chat message with an optional image attachment.
 */
export async function sendChatMessage(message: string, image?: File): Promise<ChatResponse> {
    const formData = new FormData();
    formData.append('message', message);
    if (image) {
        formData.append('image', image);
    }

    const response = await fetch(`${API_BASE_URL}/chat/`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to send message');
    }

    return response.json();
}

/**
 * Get chat history.
 */
export async function getChatHistory(): Promise<{ messages: ChatMessage[] }> {
    const response = await fetch(`${API_BASE_URL}/chat/history`);

    if (!response.ok) {
        throw new Error('Failed to fetch history');
    }

    return response.json();
}

/**
 * Transcribe audio blob to text.
 */
export async function transcribeAudio(audioBlob: Blob): Promise<string> {
    const formData = new FormData();
    formData.append('file', audioBlob, 'voice-note.webm');

    const response = await fetch(`${API_BASE_URL}/transcribe/`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to transcribe audio');
    }

    const data: TranscriptionResponse = await response.json();
    return data.text;
}

/**
 * Clear chat history.
 */
export async function clearChat(): Promise<void> {
    await fetch(`${API_BASE_URL}/chat/`, {
        method: 'DELETE',
    });
}
