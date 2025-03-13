// App.jsx
import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import ChatMessage from './components/ChatMessage';
import LLMSelector from './components/LLMSelector';
import ResponseComparison from './components/ResponseComparison';
import { fetchLLMResponses } from './services/api';

function App() {
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Welcome to LLM Response Aggregator! Ask a question and select up to 2 LLMs to compare responses.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedLLMs, setSelectedLLMs] = useState([]);
  const [lastResponse, setLastResponse] = useState(null);
  const [error, setError] = useState(null);
  const [apiMode, setApiMode] = useState(false);
  const messageEndRef = useRef(null);

  const availableLLMs = ['chatgpt', 'mistral', 'grok', 'deepseek'];

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (input.trim() === '') return;
    if (selectedLLMs.length === 0) {
      addMessage('system', 'Please select at least one LLM provider.');
      return;
    }
    if (selectedLLMs.length > 2) {
      addMessage('system', 'You can only select up to 2 LLM providers at a time.');
      return;
    }

    addMessage('user', input);
    setIsLoading(true);
    setError(null);

    try {
      let responseData;
      
      if (apiMode) {
        // Use real API
        responseData = await fetchLLMResponses(input, selectedLLMs);
      } else {
        // Use mock data for demo/development
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        responseData = {
          status_code: 200,
          detail: {
            original_query: input,
            best_response: {
              source: selectedLLMs[0],
              content: `This is a simulated response from ${selectedLLMs[0]} for the query: "${input}"\n\nHere's a simple Python function to demonstrate:\n\n\`\`\`python\ndef example():\n    print("This is an example function")\n    return True\n\`\`\``,
              score: 0.85,
              timestamp: new Date().toISOString()
            },
            all_responses: selectedLLMs.map((llm, index) => ({
              source: llm,
              content: `This is a simulated response from ${llm} for the query: "${input}"\n\nHere's a simple Python function to demonstrate:\n\n\`\`\`python\ndef example_${llm}():\n    print("This is an example function from ${llm}")\n    return True\n\`\`\``,
              score: 0.85 - (index * 0.1),
              timestamp: new Date().toISOString()
            })),
            filename: `results/llm_responses_${Date.now()}.json`
          }
        };
      }

      if (responseData.status_code !== 200) {
        throw new Error(responseData.detail || 'Error retrieving LLM responses');
      }

      setLastResponse(responseData.detail);
      addMessage('assistant', 'Here are the results from the LLMs you selected:');
    } catch (error) {
      console.error('Error:', error);
      setError(error.message);
      addMessage('system', `An error occurred: ${error.message}`);
    } finally {
      setIsLoading(false);
      setInput('');
    }
  };

  const addMessage = (role, content) => {
    setMessages(prevMessages => [...prevMessages, { role, content }]);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const toggleLLM = (llm) => {
    setSelectedLLMs(prev => 
      prev.includes(llm) 
        ? prev.filter(item => item !== llm) 
        : [...prev, llm]
    );
  };

  const toggleApiMode = () => {
    setApiMode(prev => !prev);
    addMessage('system', apiMode 
      ? 'Switched to demo mode. Responses are simulated.' 
      : 'Switched to API mode. Will connect to real LLM services.'
    );
  };

  return (
    <div className="flex flex-col h-screen bg-beige-100">
      <header className="bg-charcoal-900 text-beige-100 p-4 shadow-md">
        <div className="flex justify-between items-center max-w-4xl mx-auto">
          <div>
            <h1 className="text-2xl font-bold">LLM Response Aggregator</h1>
            <p className="text-sm opacity-80">Compare responses from multiple LLM providers</p>
          </div>
          <div className="flex items-center">
            <span className="mr-2 text-sm">{apiMode ? 'API' : 'Demo'} Mode</span>
            <button 
              onClick={toggleApiMode}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-beige-300 focus:ring-offset-2 ${apiMode ? 'bg-beige-400' : 'bg-charcoal-600'}`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  apiMode ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <div className="w-full flex flex-col max-w-4xl mx-auto bg-white shadow-lg rounded-lg my-4 overflow-hidden border border-beige-200">
          <div className="flex-1 p-4 overflow-y-auto">
            {messages.map((msg, index) => (
              <ChatMessage key={index} message={msg} />
            ))}
            
            {lastResponse && <ResponseComparison response={lastResponse} />}
            
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                <strong className="font-bold">Error: </strong>
                <span>{error}</span>
              </div>
            )}
            
            <div ref={messageEndRef} />
          </div>

          <div className="border-t border-beige-200 p-4 bg-beige-50">
            <LLMSelector 
              availableLLMs={availableLLMs} 
              selectedLLMs={selectedLLMs} 
              toggleLLM={toggleLLM} 
              maxSelection={2}
            />
            
            <div className="flex mt-2">
              <textarea
                className="flex-1 p-2 border border-beige-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-beige-500"
                placeholder="Ask a question..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
                rows={1}
              />
              <button
                className={`px-4 py-2 rounded-r-lg transition ${
                  isLoading 
                    ? 'bg-charcoal-400 text-white cursor-not-allowed' 
                    : 'bg-charcoal-800 text-beige-100 hover:bg-charcoal-900'
                }`}
                onClick={handleSend}
                disabled={isLoading}
              >
                {isLoading ? 'Processing...' : 'Send'}
              </button>
            </div>
            
            {isLoading && (
              <div className="mt-2 text-sm text-charcoal-600 flex items-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-beige-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Fetching responses... This may take a moment as we query multiple LLMs.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;