'use client';

import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Send, Image as ImageIcon, X, Loader2 } from 'lucide-react';
import { VoiceRecorder } from './voice-recorder';
import { transcribeAudio } from '@/lib/api';
import { cn } from '@/lib/utils';

interface ChatInputProps {
    onSend: (message: string, image?: File) => void;
    disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
    const [message, setMessage] = useState('');
    const [image, setImage] = useState<File | null>(null);
    const [isTranscribing, setIsTranscribing] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleSend = () => {
        if ((message.trim() || image) && !disabled) {
            onSend(message, image || undefined);
            setMessage('');
            setImage(null);
        }
    };

    const onKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleRecordingComplete = async (blob: Blob) => {
        setIsTranscribing(true);
        try {
            const text = await transcribeAudio(blob);
            setMessage(prev => prev ? `${prev} ${text}` : text);
        } catch (err) {
            console.error('Transcription failed:', err);
        } finally {
            setIsTranscribing(false);
        }
    };

    const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setImage(e.target.files[0]);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-4 bg-white border-t sm:border border-gray-100 sm:rounded-2xl sm:shadow-lg sm:mb-8 transition-all">
            {/* Image Preview */}
            {image && (
                <div className="mb-3 relative inline-block group">
                    <img
                        src={URL.createObjectURL(image)}
                        alt="Preview"
                        className="h-20 w-auto rounded-lg border border-gray-200"
                    />
                    <button
                        onClick={() => setImage(null)}
                        className="absolute -top-2 -right-2 bg-gray-800 text-white rounded-full p-1 shadow-md opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        <X className="h-3 w-3" />
                    </button>
                </div>
            )}

            <div className="flex items-end gap-2">
                {/* Attachment Button */}
                <input
                    type="file"
                    ref={fileInputRef}
                    className="hidden"
                    accept="image/*"
                    onChange={handleImageSelect}
                />
                <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    className="rounded-full text-gray-500 hover:text-indigo-600"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={disabled || !!image}
                >
                    <ImageIcon className="h-5 w-5" />
                </Button>

                {/* Voice Recorder */}
                <VoiceRecorder
                    onRecordingComplete={handleRecordingComplete}
                    disabled={disabled || isTranscribing}
                />

                {/* Text Input */}
                <div className="flex-1 relative">
                    <textarea
                        className="w-full bg-gray-50 border-none focus:ring-2 focus:ring-indigo-500 rounded-xl px-4 py-3 text-sm resize-none max-h-32 transition-all placeholder:text-gray-400"
                        rows={1}
                        placeholder={isTranscribing ? "Transcribing voice..." : "Ask RIZZA for advice or attach a screenshot..."}
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={onKeyDown}
                        disabled={disabled || isTranscribing}
                    />
                </div>

                {/* Send Button */}
                <Button
                    type="button"
                    size="icon"
                    className={cn(
                        "rounded-full h-10 w-10 bg-indigo-600 hover:bg-indigo-700 shadow-md transition-all active:scale-90",
                        (!message.trim() && !image) && "opacity-50 cursor-not-allowed"
                    )}
                    onClick={handleSend}
                    disabled={disabled || (!message.trim() && !image) || isTranscribing}
                >
                    {disabled ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                </Button>
            </div>
        </div>
    );
}
