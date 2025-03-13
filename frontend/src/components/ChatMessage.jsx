// components/ChatMessage.jsx
import React from 'react';

const ChatMessage = ({ message }) => {
  const { role, content } = message;
  
  let bgColor = 'bg-white';
  let textColor = 'text-charcoal-800';
  let borderColor = 'border-beige-200';
  let alignClass = 'justify-start';
  let avatar = '🤖';

  if (role === 'user') {
    bgColor = 'bg-beige-200';
    borderColor = 'border-beige-300';
    alignClass = 'justify-end';
    avatar = '👤';
  } else if (role === 'system') {
    bgColor = 'bg-charcoal-100';
    textColor = 'text-charcoal-700';
    borderColor = 'border-charcoal-200';
    avatar = '🔔';
  }

  return (
    <div className={`flex ${alignClass} mb-4`}>
      <div className={`max-w-3/4 ${bgColor} rounded-lg p-3 shadow-sm border ${borderColor}`}>
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