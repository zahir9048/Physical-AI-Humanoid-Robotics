import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '../services/types';
import ChatAPI from '../services/ChatAPI';
import { ThumbsUp, ThumbsDown } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
  avatar: React.ReactNode;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, avatar }) => {
  const isUser = message.role === 'user';
  const [feedback, setFeedback] = useState<{ rating: -1 | 0 | 1 | null }>({ rating: null });

  // Extract citations from message content if it exists
  // For now, we'll assume citations are passed in the source_chunks or as part of the message
  // In a full implementation, this would be properly parsed from the backend response
  const citations = message.source_chunks || [];

  const handleFeedback = async (rating: -1 | 0 | 1) => {
    if (feedback.rating === rating) {
      // If clicking the same rating, reset to neutral
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
      // Revert feedback if submission failed
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
        <ReactMarkdown className={`prose ${isUser ? 'text-white' : 'text-gray-800'}`}>
          {message.content}
        </ReactMarkdown>

        {/* Display citations if any exist */}
        {citations.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-300">
            <p className="text-xs font-semibold text-gray-600 mb-1">Sources:</p>
            <ul className="text-xs text-gray-600">
              {citations.slice(0, 3).map((chunkId, index) => (
                <li key={index} className="truncate">• {chunkId}</li>
              ))}
              {citations.length > 3 && (
                <li className="text-xs text-gray-500">• ... and {citations.length - 3} more</li>
              ))}
            </ul>
          </div>
        )}

        {/* Feedback controls for assistant messages */}
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