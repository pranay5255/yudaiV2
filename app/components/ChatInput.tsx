import React, { useState, useRef, useEffect } from 'react';
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
  datasetProfile, 
}) => {
  const [message, setMessage] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestionPosition, setSuggestionPosition] = useState({ top: 0, left: 0 });
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (message.endsWith('/')) {
      const rect = inputRef.current?.getBoundingClientRect();
      if (rect) {
        setSuggestionPosition({
          top: rect.top - (rect.height + 10),
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
    <div className="relative w-full">
      <form onSubmit={handleSubmit} className="flex items-end gap-2">
        <textarea
          ref={inputRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={datasetProfile ? "Type / for analysis commands..." : "Upload a dataset to begin analysis..."}
          className="flex-1 resize-none rounded-lg bg-gray-700 p-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[50px]"
          rows={1}
          disabled={disabled || !datasetProfile}
        />
        <button
          type="submit"
          disabled={disabled || !message.trim() || !datasetProfile}
          className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </form>

      {showSuggestions && datasetProfile && (
        <div className="fixed inset-0 bg-black bg-opacity-20 z-40">
          <CommandSuggestions
            isVisible={showSuggestions}
            position={suggestionPosition}
            onSelect={handleCommandSelect}
            datasetProfile={datasetProfile}
          />
        </div>
      )}
    </div>
  );
}; 