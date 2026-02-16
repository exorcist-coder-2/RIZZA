'use client';

import { useState, useEffect, useRef } from 'react';
import { ChatMessage as ChatMessageComponent } from '@/components/chat-message';
import { ChatInput } from '@/components/chat-input';
import {
  getChatHistory,
  sendChatMessage,
  clearChat,
  ChatMessage as ChatMessageType
} from '@/lib/api';
import {
  Brain,
  Sparkles,
  Trash2,
  Settings,
  MessageCircle,
  Clock
} from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function Home() {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [loading, setLoading] = useState(false);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Load history on mount
  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await getChatHistory();
        setMessages(data.messages);
      } catch (err) {
        console.error('Failed to load history:', err);
      } finally {
        setIsInitialLoading(false);
      }
    }
    loadHistory();
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleSend = async (text: string, image?: File) => {
    // Add optimistic user message
    const optimisticMsg: ChatMessageType = {
      id: Date.now(),
      role: 'user',
      content: text || "[Sent an image]",
      created_at: new Date().toISOString()
    };

    setMessages(prev => [...prev, optimisticMsg]);
    setLoading(true);

    try {
      const result = await sendChatMessage(text, image);

      // Replace with actual data from backend
      const assistantMsg: ChatMessageType = {
        id: Date.now() + 1,
        role: 'assistant',
        content: result.response,
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMsg]);
    } catch (err) {
      console.error('Chat error:', err);
      // Add error message
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: "Sorry, I lost my connection for a moment. Please try again!",
        created_at: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = async () => {
    if (confirm("Are you sure you want to clear our strategy session?")) {
      await clearChat();
      setMessages([]);
    }
  };

  return (
    <main className="flex flex-col h-screen bg-white">
      {/* Header */}
      <header className="flex-shrink-0 border-b border-gray-100 bg-white/80 backdrop-blur-md z-10 sticky top-0">
        <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-indigo-600 p-1.5 rounded-lg">
              <Brain className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900 leading-none">RIZZA</h1>
              <p className="text-[10px] text-gray-500 font-medium tracking-widest uppercase mt-0.5">Messaging Strategist</p>
            </div>
          </div>

          <div className="flex items-center gap-1">
            <Button variant="ghost" size="icon" className="text-gray-400 hover:text-red-500" onClick={handleClearChat}>
              <Trash2 className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" className="text-gray-400">
              <Settings className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto" ref={scrollRef}>
        <div className="max-w-4xl mx-auto px-4 py-8">
          {/* Welcome Message */}
          {messages.length === 0 && !isInitialLoading && (
            <div className="py-12 flex flex-col items-center text-center animate-in fade-in zoom-in duration-500">
              <div className="w-16 h-16 bg-indigo-50 rounded-full flex items-center justify-center mb-6">
                <Sparkles className="h-8 w-8 text-indigo-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome to RIZZA</h2>
              <p className="text-gray-500 max-w-sm">
                I&apos;m your AI Messaging Strategist. Share a screenshot of a chat, record a voice note, or tell me about your situation.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-10 w-full max-w-lg">
                {[
                  "How should I reply to this?",
                  "Analyze our conversation tone",
                  "What does this text really mean?",
                  "Help me initiate a chat"
                ].map(prompt => (
                  <button
                    key={prompt}
                    onClick={() => handleSend(prompt)}
                    className="p-3 text-sm text-gray-600 bg-gray-50 hover:bg-indigo-50 hover:text-indigo-600 border border-gray-100 rounded-xl transition-all text-left flex items-center gap-2"
                  >
                    <MessageCircle className="h-4 w-4 opacity-50" />
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          <div className="space-y-2">
            {messages.map((msg) => (
              <ChatMessageComponent key={msg.id} message={msg} />
            ))}

            {/* Thinking Indicator */}
            {loading && (
              <div className="flex justify-start mb-6 animate-in fade-in duration-300">
                <div className="flex-shrink-0 h-8 w-8 rounded-full bg-indigo-50 flex items-center justify-center mt-1 outline outline-2 outline-indigo-100 outline-offset-2">
                  <Brain className="h-4 w-4 text-indigo-600 animate-pulse" />
                </div>
                <div className="mx-3 px-4 py-3 rounded-2xl bg-gray-50 border border-gray-100 rounded-tl-none">
                  <div className="flex gap-1">
                    <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce [animation-delay:-0.3s]" />
                    <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce [animation-delay:-0.15s]" />
                    <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce" />
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Input Section */}
      <footer className="flex-shrink-0 z-20">
        <ChatInput onSend={handleSend} disabled={loading} />
      </footer>
    </main>
  );
}
