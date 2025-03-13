// components/ChatMessage.jsx
import React from 'react';

const ChatMessage = ({ message }) => {
  const { role, content } = message;
  
  let bgColor = 'bg-white';
  let textColor = 'text-gray-800';
  let alignClass = 'justify-start';
  let avatar = '🤖';

  if (role === 'user') {
    bgColor = 'bg-blue-100';
    alignClass = 'justify-end';
    avatar = '👤';
  } else if (role === 'system') {
    bgColor = 'bg-gray-100';
    textColor = 'text-gray-600';
    avatar = '🔔';
  }

  return (
    <div className={`flex ${alignClass} mb-4`}>
      <div className={`max-w-3/4 ${bgColor} rounded-lg p-3 shadow-sm`}>
        <div className="flex items-center mb-1">
          <span className="mr-2">{avatar}</span>
          <span className="font-semibold capitalize">{role}</span>
        </div>
        <div className={`${textColor} whitespace-pre-wrap`}>
          {content}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;