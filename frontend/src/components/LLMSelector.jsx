// components/LLMSelector.jsx
import React from 'react';

const LLMSelector = ({ availableLLMs, selectedLLMs, toggleLLM, maxSelection = 2 }) => {
  return (
    <div className="mb-3">
      <p className="text-sm text-gray-600 mb-2">
        Select up to {maxSelection} LLM provider{maxSelection !== 1 ? 's' : ''}:
      </p>
      <div className="flex flex-wrap gap-2">
        {availableLLMs.map(llm => {
          const isSelected = selectedLLMs.includes(llm);
          const isDisabled = !isSelected && selectedLLMs.length >= maxSelection;
          
          return (
            <button
              key={llm}
              onClick={() => !isDisabled && toggleLLM(llm)}
              className={`px-3 py-1 rounded-full text-sm transition ${
                isSelected
                  ? 'bg-blue-600 text-white'
                  : isDisabled
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
              }`}
              disabled={isDisabled}
            >
              <span className="capitalize">{llm}</span>
              {isSelected && ' ✓'}
            </button>
          );
        })}
      </div>
      {selectedLLMs.length > maxSelection && (
        <p className="text-xs text-red-500 mt-1">
          Please select only up to {maxSelection} LLM provider{maxSelection !== 1 ? 's' : ''}.
        </p>
      )}
    </div>
  );
};

export default LLMSelector;
