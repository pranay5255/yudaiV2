import React from 'react';
import { DatasetProfile } from '../../codegen/app/models';

interface CommandSuggestionsProps {
  isVisible: boolean;
  position: { top: number; left: number };
  onSelect: (command: string) => void;
  datasetProfile: DatasetProfile;
}

interface CommandOption {
  command: string;
  description: string;
}

const commands: CommandOption[] = [
  {
    command: '/transform',
    description: 'Perform CRUD operations on the dataset'
  },
  {
    command: '/lookup',
    description: 'Search and visualize specific data conditions'
  },
  {
    command: '/scratchpad',
    description: 'Add relevant information to research notes'
  }
];

export const CommandSuggestions: React.FC<CommandSuggestionsProps> = ({
  isVisible,
  position,
  onSelect,
}) => {
  if (!isVisible) return null;

  return (
    <div
      className="absolute z-100 bg-gray-800 rounded-lg shadow-lg border border-gray-700 w-100 max-h-[30px] overflow-y-auto"
      style={{
        top: `${position.top}px`,
        left: `${position.left}px`,
      }}
    >
      <ul className="py-2">
        {commands.map((cmd) => (
          <li
            key={cmd.command}
            className="px-4 py-2 hover:bg-gray-700 cursor-pointer flex flex-col"
            onClick={() => onSelect(cmd.command)}
          >
            <span className="text-blue-400 font-medium">{cmd.command}</span>
            <span className="text-gray-400 text-sm">{cmd.description}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}; 