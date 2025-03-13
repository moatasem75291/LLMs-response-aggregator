// components/ResponseComparison.jsx
import React, { useState } from 'react';
import { formatTimestamp, formatScore } from '../utils/formatters';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vs } from 'react-syntax-highlighter/dist/esm/styles/prism';

const ResponseComparison = ({ response }) => {
  const [activeTab, setActiveTab] = useState('best');
  
  if (!response) return null;
  
  const { best_response, all_responses } = response;

  // Function to format response content with code highlighting
  const formatContent = (content) => {
    if (!content) return null;
    
    // Split by code blocks
    const parts = content.split(/```(\w*)\n/);
    
    if (parts.length <= 1) {
      // No code blocks, return plain text
      return <div className="whitespace-pre-wrap">{content}</div>;
    }
    
    // Assemble the parts with code highlighting
    return parts.map((part, index) => {
      // Even indices are text, odd indices are language markers, following indices are code
      if (index % 3 === 0) {
        return part ? <div key={index} className="whitespace-pre-wrap mb-2">{part}</div> : null;
      } else if (index % 3 === 1) {
        // This is a language marker, skip it
        return null;
      } else {
        const language = parts[index - 1] || 'text';
        return (
          <SyntaxHighlighter 
            key={index} 
            language={language} 
            style={vs}
            className="rounded mb-2"
          >
            {part}
          </SyntaxHighlighter>
        );
      }
    });
  };
  
  return (
    <div className="border border-beige-200 rounded-lg overflow-hidden mb-4 bg-white">
      <div className="flex border-b border-beige-200">
        <button 
          className={`flex-1 py-2 px-4 ${activeTab === 'best' 
            ? 'bg-beige-100 border-b-2 border-beige-500 text-charcoal-800' 
            : 'text-charcoal-600 hover:bg-beige-50'}`}
          onClick={() => setActiveTab('best')}
        >
          Best Response
        </button>
        <button 
          className={`flex-1 py-2 px-4 ${activeTab === 'all' 
            ? 'bg-beige-100 border-b-2 border-beige-500 text-charcoal-800' 
            : 'text-charcoal-600 hover:bg-beige-50'}`}
          onClick={() => setActiveTab('all')}
        >
          All Responses
        </button>
      </div>
      
      <div className="p-4">
        {activeTab === 'best' ? (
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center">
                <div className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm mr-2 capitalize font-semibold">
                  {best_response.source}
                </div>
                <div className="text-sm text-charcoal-600">
                  Score: {formatScore(best_response.score)}
                </div>
              </div>
              <div className="text-xs text-charcoal-500">
                {formatTimestamp(best_response.timestamp)}
              </div>
            </div>
            <div className="p-4 bg-beige-50 rounded border border-beige-200">
              {formatContent(best_response.content)}
            </div>
          </div>
        ) : (
          <div>
            {all_responses.map((resp, index) => (
              <div 
                key={index} 
                className={`mb-6 last:mb-0 ${index !== all_responses.length - 1 ? 'pb-6 border-b border-beige-200' : ''}`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center">
                    <div 
                      className={`px-2 py-1 rounded text-sm mr-2 capitalize font-semibold
                        ${resp.source === best_response.source 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-beige-200 text-charcoal-800'}`}
                    >
                      {resp.source}
                      {resp.source === best_response.source && ' (Best)'}
                    </div>
                    <div className="text-sm text-charcoal-600">
                      Score: {formatScore(resp.score)}
                    </div>
                  </div>
                  <div className="text-xs text-charcoal-500">
                    {formatTimestamp(resp.timestamp)}
                  </div>
                </div>
                <div className="p-4 bg-beige-50 rounded border border-beige-200">
                  {formatContent(resp.content)}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResponseComparison;