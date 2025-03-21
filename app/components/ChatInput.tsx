import React, { useState, useRef } from 'react';
import { CommandSuggestions } from './CommandSuggestions';
import { DatasetProfile } from '../../codegen/app/models';

interface ChatInputProps {
  onSubmit: (message: string) => void;
  disabled?: boolean;
  datasetProfile?: DatasetProfile;
  messages: Array<{ text: string; isUser: boolean }>;
}

export const ChatInput: React.FC<ChatInputProps> = ({ 
  onSubmit, 
  disabled, 
  datasetProfile 
}) => {
  const [message, setMessage] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestionPosition, setSuggestionPosition] = useState({ top: 0, left: 0 });
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSubmit(message);
      setMessage('');
      setShowSuggestions(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newMessage = e.target.value;
    setMessage(newMessage);

    // Show suggestions when typing /
    if (newMessage.endsWith('/')) {
      const rect = inputRef.current?.getBoundingClientRect();
      if (rect) {
        setSuggestionPosition({
          top: rect.top - 1000,
          left: rect.left - 300
        });
      }
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  };

  return (
    <div className="relative w-full">
      <form onSubmit={handleSubmit} className="flex items-end gap-2">
        <textarea
          ref={inputRef}
          value={message}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder={datasetProfile ? "Type / for commands or enter your message..." : "Upload a dataset to begin analysis..."}
          className="flex-1 rounded-lg bg-gray-700 p-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[50px] max-h-[150px]"
          disabled={disabled || !datasetProfile}
        />
        <button
          type="submit"
          disabled={disabled || !message.trim() || !datasetProfile}
          className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed h-[50px]"
        >
          Send
        </button>
      </form>

      {showSuggestions && datasetProfile && (
        <CommandSuggestions
          isVisible={showSuggestions}
          position={suggestionPosition}
          onSelect={(command) => {
            setMessage(command + ' ');
            setShowSuggestions(false);
            inputRef.current?.focus();
          }}
          datasetProfile={datasetProfile}
        />
      )}
    </div>
  );
};