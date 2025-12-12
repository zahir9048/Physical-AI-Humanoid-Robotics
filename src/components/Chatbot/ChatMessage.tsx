import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '../../services/types';
import ChatAPI from '../../services/ChatAPI';
import { ThumbsUp, ThumbsDown } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
  avatar: React.ReactNode;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, avatar }) => {
  const isUser = message.role === 'user';
  const [feedback, setFeedback] = useState<{ rating: -1 | 0 | 1 | null }>({ rating: null });

  const citations = message.source_chunks || [];

  // Format timestamp
  const formatTimestamp = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const messageDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
      
      // Check if it's today
      if (messageDate.getTime() === today.getTime()) {
        // Show only time for today
        return date.toLocaleTimeString('en-US', { 
          hour: 'numeric', 
          minute: '2-digit',
          hour12: true 
        });
      } else {
        // Show date and time for older messages
        return date.toLocaleString('en-US', {
          month: 'short',
          day: 'numeric',
          hour: 'numeric',
          minute: '2-digit',
          hour12: true
        });
      }
    } catch (error) {
      return '';
    }
  };

  const formattedTime = message.timestamp ? formatTimestamp(message.timestamp) : '';

  const handleFeedback = async (rating: -1 | 0 | 1) => {
    if (feedback.rating === rating) {
      setFeedback({ rating: 0 });
      return;
    }

    setFeedback({ rating });

    try {
      await ChatAPI.submitFeedback({
        message_id: message.id,
        rating: rating,
      });
    } catch (error) {
      console.error('Error submitting feedback:', error);
      setFeedback(prev => ({ rating: prev.rating === rating ? 0 : rating }));
    }
  };

  return (
    <div className={`flex items-start mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="bg-blue-100 rounded-full p-2 mr-3">
          {avatar}
        </div>
      )}

      <div className={`max-w-[80%] ${isUser ? 'bg-blue-500 text-white' : 'bg-gray-200'} rounded-lg p-3`}>
        <div className={`prose ${isUser ? 'text-white' : 'text-gray-800'}`}>
          <ReactMarkdown>
            {message.content}
          </ReactMarkdown>
        </div>

        {formattedTime && (
          <div className={`text-xs mt-2 ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
            {formattedTime}
          </div>
        )}

        {citations.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-300">
            <p className="text-xs font-semibold text-gray-600 mb-1">Sources:</p>
            <ul className="text-xs text-gray-600">
              {citations.slice(0, 3).map((chunkId, index) => (
                <li key={index} className="truncate">• {chunkId}</li>
              ))}
              {citations.length > 3 && (
                <li className="text-xs text-gray-500">• ... and {citations.length - 3} more</li>
              )}
            </ul>
          </div>
        )}

        {!isUser && (
          <div className="mt-2 flex items-center space-x-2">
            <button
              onClick={() => handleFeedback(1)}
              className={`p-1 rounded ${feedback.rating === 1 ? 'text-green-600 bg-green-100' : 'text-gray-500 hover:text-green-600'}`}
              title="Thumbs up - helpful"
            >
              <ThumbsUp size={14} />
            </button>
            <button
              onClick={() => handleFeedback(-1)}
              className={`p-1 rounded ${feedback.rating === -1 ? 'text-red-600 bg-red-100' : 'text-gray-500 hover:text-red-600'}`}
              title="Thumbs down - not helpful"
            >
              <ThumbsDown size={14} />
            </button>
          </div>
        )}
      </div>

      {isUser && (
        <div className="bg-blue-500 rounded-full p-2 ml-3">
          {avatar}
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
