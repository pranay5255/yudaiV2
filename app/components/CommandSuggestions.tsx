import React from 'react';
import { DatasetProfile } from '../../codegen/app/models';

interface CommandSuggestionsProps {
  isVisible: boolean;
  position: { top: number; left: number };
  onSelect: (command: string) => void;
  datasetProfile: DatasetProfile;
}

interface Command {
  command: string;
  description: string;
  available: (profile: DatasetProfile) => boolean;
}

const commands: Command[] = [
  {
    command: '/analyze',
    description: 'Get a general analysis of the dataset',
    available: () => true
  },
  {
    command: '/trend',
    description: 'Analyze trends over time',
    available: (profile) => Object.values(profile.variables).some(v => v.type === 'DateTime')
  },
  {
    command: '/correlate',
    description: 'Find correlations between variables',
    available: (profile) => Object.values(profile.variables).some(v => v.type === 'Numeric')
  },
  {
    command: '/missing',
    description: 'Analyze missing values',
    available: (profile) => profile.table.n_cells_missing > 0
  },
  {
    command: '/duplicates',
    description: 'Find and analyze duplicate rows',
    available: (profile) => profile.table.n_duplicates > 0
  },
  {
    command: '/distribution',
    description: 'Show value distributions',
    available: () => true
  }
];

export const CommandSuggestions: React.FC<CommandSuggestionsProps> = ({
  isVisible,
  position,
  onSelect,
  datasetProfile
}) => {
  if (!isVisible) return null;

  const availableCommands = commands.filter(cmd => cmd.available(datasetProfile));

  return (
    <div
      className="fixed z-50 bg-gray-800 rounded-lg shadow-lg border border-gray-700 max-h-96 overflow-y-auto w-80"
      style={{ top: position.top, left: position.left }}
    >
      {availableCommands.map((cmd) => (
        <div
          key={cmd.command}
          className="p-3 hover:bg-gray-700 cursor-pointer border-b border-gray-700 last:border-b-0"
          onClick={() => onSelect(cmd.command)}
        >
          <div className="flex flex-col">
            <span className="text-blue-400 font-mono text-sm">{cmd.command}</span>
            <span className="text-gray-400 text-xs mt-1">{cmd.description}</span>
          </div>
        </div>
      ))}
    </div>
  );
};