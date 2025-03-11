import React, { useState, useRef, useEffect } from 'react';
import { CommandSuggestions } from './CommandSuggestions';

interface ChatInputProps {
  onSubmit: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSubmit, disabled }) => {
  const [message, setMessage] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestionPosition, setSuggestionPosition] = useState({ top: 0, left: 0 });
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (message.endsWith('/')) {
      const rect = inputRef.current?.getBoundingClientRect();
      if (rect) {
        setSuggestionPosition({
          top: rect.top ,
          left: rect.left
        });
      }
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  }, [message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSubmit(message);
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleCommandSelect = (command: string) => {
    setMessage(command + ' ');
    setShowSuggestions(false);
    inputRef.current?.focus();
  };

  return (
    <div className="relative">
      <form onSubmit={handleSubmit} className="flex items-end gap-2">
        <textarea
          ref={inputRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type / for commands or enter your message..."
          className="flex-1 resize-none rounded-lg bg-gray-700 p-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={1}
          disabled={disabled}
        />
        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:bg-gray-600"
        >
          Send
        </button>
      </form>

      {showSuggestions && (
        <div className="fixed inset-0 bg-black bg-opacity-20 z-40">
          <CommandSuggestions
            isVisible={showSuggestions}
            position={suggestionPosition}
            onSelect={handleCommandSelect}
          />
        </div>
      )}
    </div>
  );
}; 