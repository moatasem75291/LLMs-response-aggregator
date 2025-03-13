// components/LLMSelector.jsx
import React from 'react';

const LLMSelector = ({ availableLLMs, selectedLLMs, toggleLLM, maxSelection = 2 }) => {
  return (
    <div className="mb-3">
      <p className="text-sm text-charcoal-600 mb-2">
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
                  ? 'bg-charcoal-800 text-beige-100'
                  : isDisabled
                    ? 'bg-beige-100 text-charcoal-400 cursor-not-allowed'
                    : 'bg-beige-200 text-charcoal-800 hover:bg-beige-300'
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