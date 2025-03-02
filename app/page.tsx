"use client";

import { useState } from "react";

export default function Home() {
  const [messages, setMessages] = useState<Array<{ text: string; isUser: boolean }>>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message
    setMessages(prev => [...prev, { text: inputMessage, isUser: true }]);
    
    // Simulate bot response (you can replace this with actual API call)
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        text: "This is a demo response. Replace with actual chatbot integration!", 
        isUser: false 
      }]);
    }, 1000);

    setInputMessage("");
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    if (!file.name.endsWith('.csv')) {
      alert('Please upload a CSV file');
      return;
    }

    setFile(file);
    setIsUploading(true);
    
    // Add a message to show the file is being processed
    setMessages(prev => [...prev, { 
      text: `Processing file: ${file.name}`, 
      isUser: false 
    }]);

    // Here you would typically upload the file to your server
    // For now, we'll just simulate a response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        text: `Successfully processed ${file.name}! You can now start asking questions about your data.`, 
        isUser: false 
      }]);
      setIsUploading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col">
      {/* Header with file upload */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-white">Data Analysis Assistant</h1>
          <div className="flex items-center gap-4">
            <label className="relative cursor-pointer">
              <input
                type="file"
                accept=".csv"
                onChange={handleFileUpload}
                className="hidden"
                disabled={isUploading}
              />
              <span className={`px-4 py-2 rounded-lg text-white ${isUploading 
                ? 'bg-gray-600' 
                : 'bg-blue-600 hover:bg-blue-700'} transition-colors`}>
                {isUploading ? 'Uploading...' : 'Upload CSV'}
              </span>
            </label>
            {file && (
              <span className="text-gray-300 text-sm">
                File: {file.name}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col max-w-7xl w-full mx-auto p-4">
        {/* Chat messages */}
        <div className="flex-1 overflow-y-auto mb-4 p-4 rounded-lg bg-gray-800 border border-gray-700">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`mb-4 ${
                message.isUser ? "text-right" : "text-left"
              }`}
            >
              <div
                className={`inline-block p-3 rounded-lg max-w-[80%] ${
                  message.isUser
                    ? "bg-blue-600 text-white"
                    : "bg-gray-700 text-gray-100"
                }`}
              >
                {message.text}
              </div>
            </div>
          ))}
        </div>

        {/* Message input */}
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask about your data..."
            className="flex-1 p-3 bg-gray-800 text-white border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400"
          />
          <button
            type="submit"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
} 