import { useState } from 'react';
import { cn } from '@/lib/utils';
import { ChatMessage as ChatMessageType } from '@/lib/api';
import { Sparkles, User, Brain, Copy, Check } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
    message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
    const isAI = message.role === 'assistant';

    return (
        <div className={cn(
            "flex w-full mb-6 animate-in fade-in slide-in-from-bottom-2 duration-300",
            isAI ? "justify-start" : "justify-end"
        )}>
            <div className={cn(
                "flex max-w-[85%] sm:max-w-[75%]",
                isAI ? "flex-row" : "flex-row-reverse"
            )}>
                {/* Avatar */}
                <div className={cn(
                    "flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center mt-1 outline outline-2 outline-offset-2",
                    isAI
                        ? "bg-gradient-to-br from-indigo-600 to-purple-600 text-white outline-indigo-200"
                        : "bg-gray-200 text-gray-600 outline-gray-100"
                )}>
                    {isAI ? <Brain className="h-4 w-4" /> : <User className="h-4 w-4" />}
                </div>

                {/* Bubble */}
                <div className={cn(
                    "mx-3 px-4 py-3 rounded-2xl shadow-sm text-sm overflow-hidden group relative",
                    isAI
                        ? "bg-white border border-gray-100 text-gray-800 rounded-tl-none pr-8"
                        : "bg-indigo-600 text-white rounded-tr-none"
                )}>
                    {isAI ? (
                        <div className="prose prose-sm prose-p:leading-relaxed prose-pre:bg-gray-800 prose-pre:text-gray-100">
                            <ReactMarkdown>{message.content}</ReactMarkdown>
                            <CopyButton text={message.content} />
                        </div>
                    ) : (
                        <div className="whitespace-pre-wrap leading-relaxed">
                            {message.content}
                        </div>
                    )}

                    <div className={cn(
                        "mt-1 text-[10px] flex items-center gap-1 opacity-50 font-medium uppercase tracking-tighter",
                        isAI ? "text-gray-400" : "text-indigo-200"
                    )}>
                        {new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        {message.is_voice && <span className="flex items-center gap-1">• Voice</span>}
                    </div>
                </div>
            </div>
        </div>
    );
}

function CopyButton({ text }: { text: string }) {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(text);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            console.error('Failed to copy keys', err);
        }
    };

    return (
        <button
            onClick={handleCopy}
            className="absolute top-2 right-2 p-1.5 rounded-lg text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 opacity-0 group-hover:opacity-100 transition-all"
            title="Copy to clipboard"
        >
            {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
        </button>
    );
}
