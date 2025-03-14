import React from 'react';

interface CommandSuggestionsProps {
  isVisible: boolean;
  position: { top: number; left: number };
  onSelect: (command: string) => void;
}

const commands = [
  {
    command: '/transform',
    description: 'Modify or create columns'
  },
  {
    command: '/trend', 
    description: 'Analyze trends over time'
  },
  {
    command: '/merge',
    description: 'Combine datasets'
  },
  {
    command: '/pivot',
    description: 'Reshape data'
  },
  {
    command: '/split',
    description: 'Divide data'
  },
  {
    command: '/join',
    description: 'Combine text or data'
  }
];

export const CommandSuggestions: React.FC<CommandSuggestionsProps> = ({
  isVisible,
  position,
  onSelect
}) => {
  if (!isVisible) return null;

  return (
    <div
      className="fixed z-50 bg-gray-800 rounded-lg shadow-lg border border-gray-700 max-h-96"
      style={{ top: position.top, left: position.left }}
    >
      {commands.map((cmd) => (
        <div
          key={cmd.command}
          className="p-2 hover:bg-gray-700 cursor-pointer border-b border-gray-700 last:border-b-0"
          onClick={() => onSelect(cmd.command)}
        >
          <div className="flex items-center">
            <span className="text-blue-400 font-mono">{cmd.command}</span>
            <span className="p-3 ml-4 text-gray-400 text-sm">{cmd.description}</span>
          </div>
        </div>
      ))}
    </div>
  );
};