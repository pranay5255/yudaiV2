"use client";

import { useState } from "react";
import { useRouter } from 'next/navigation';
import { ChatInput } from './components/ChatInput';
import { Sidebar } from './components/Sidebar';
import { DatasetProfile } from '../codegen/app/models';
import { useDataset } from './context/DatasetContext';

export default function Home() {
    const router = useRouter();
    const { datasetStats, setDatasetStats } = useDataset();
    const [messages, setMessages] = useState<Array<{ text: string; isUser: boolean }>>([]);
    const [file, setFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);

    const handleSubmit = async (message: string) => {
        if (!message.trim() || !datasetStats) return;

        // Add user message
        setMessages(prev => [...prev, { text: message, isUser: true }]);
        
        try {
            const response = await fetch('/api/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to get response from chat API');
            }
            
            const result = await response.json();
            
            // Add assistant's response
            setMessages(prev => [...prev, { 
                text: result.message + (result.code ? `\n\n\`\`\`python\n${result.code}\n\`\`\`` : ''), 
                isUser: false 
            }]);
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            setMessages(prev => [...prev, { 
                text: `Error: ${errorMessage}`, 
                isUser: false 
            }]);
        }
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
        
        // Send file to API for processing
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/process-file', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error || 'Failed to process file');
            }

            // Convert timestamp string to Date object before setting state
            const processedData: DatasetProfile = {
                ...result.data,
                timestamp: new Date(result.data.timestamp)
            };
            setDatasetStats(processedData);
            
            setMessages(prev => [...prev, { 
                text: `Successfully processed ${file.name}! You can now start asking questions about your data.`, 
                isUser: false 
            }]);
        } catch (error: unknown) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            setMessages(prev => [...prev, { 
                text: `Error processing file: ${errorMessage}`, 
                isUser: false 
            }]);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 flex">
            {datasetStats && <Sidebar datasetStats={datasetStats} />}
            <div className="flex-1 flex flex-col">
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
                            <button
                                onClick={() => router.push('/datag')}
                                className="px-4 py-2 rounded-lg text-white bg-green-600 hover:bg-green-700 transition-colors"
                                disabled={!datasetStats}
                            >
                                Data Graph
                            </button>
                            {file && (
                                <span className="text-gray-300 text-sm">
                                    File: {file.name}
                                </span>
                            )}
                        </div>
                    </div>
                </div>

                {/* Main chat area */}
                <div className="flex-1 overflow-y-auto p-4">
                    <div className="max-w-7xl mx-auto space-y-4">
                        {messages.map((msg, i) => (
                            <div
                                key={i}
                                className={`p-4 rounded-lg ${
                                    msg.isUser ? 'bg-blue-600 ml-auto' : 'bg-gray-800'
                                } max-w-[80%]`}
                            >
                                <p className="text-white">{msg.text}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Chat input with command suggestions */}
                <div className="border-t border-gray-700 p-4">
                    <div className="max-w-7xl mx-auto">
                        <ChatInput
                            onSubmit={handleSubmit}
                            disabled={isUploading || !datasetStats}
                            datasetProfile={datasetStats || undefined}
                            messages={messages}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
} 