import React, { useState, KeyboardEvent, useEffect, useRef } from 'react';
import { Send, Mic, X } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled: boolean;
  placeholder?: string;
  onListeningChange?: (isListening: boolean) => void;
}

// Extend Window interface for Web Speech API
declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled, placeholder = 'Type your message...', onListeningChange }) => {
  const [inputValue, setInputValue] = useState('');
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);
  const accumulatedTranscriptRef = useRef<string>('');

  useEffect(() => {
    // Notify parent component of listening state change
    if (onListeningChange) {
      onListeningChange(isListening);
    }
  }, [isListening, onListeningChange]);

  useEffect(() => {
    // Initialize Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true; // Keep listening until manually stopped
      recognition.interimResults = true; // Show interim results
      recognition.lang = 'en-US'; // Set to English

      recognition.onstart = () => {
        setIsListening(true);
        // Start with current input value
        accumulatedTranscriptRef.current = inputValue || '';
      };

      recognition.onresult = (event: any) => {
        // Accumulate all results
        let interimTranscript = '';
        let finalTranscript = accumulatedTranscriptRef.current;

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += (finalTranscript ? ' ' : '') + transcript;
            accumulatedTranscriptRef.current = finalTranscript;
          } else {
            interimTranscript += transcript;
          }
        }

        // Update input with final + interim transcript
        setInputValue(finalTranscript + interimTranscript);
      };

      recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        // Don't stop on error, just log it
        if (event.error === 'no-speech') {
          // This is normal, just continue listening
          return;
        }
      };

      recognition.onend = () => {
        // Only stop if we manually stopped it (isListening will be false)
        if (isListening) {
          // Restart if it ended unexpectedly
          try {
            recognition.start();
          } catch (error) {
            setIsListening(false);
          }
        }
      };

      recognitionRef.current = recognition;
    }

    // Cleanup
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const handleSubmit = () => {
    if (inputValue.trim() && !disabled) {
      // Stop recording if active
      if (isListening && recognitionRef.current) {
        recognitionRef.current.stop();
        setIsListening(false);
        accumulatedTranscriptRef.current = '';
      }
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
      return;
    }

    if (isListening) {
      // Stop recording manually
      recognitionRef.current.stop();
      setIsListening(false);
      accumulatedTranscriptRef.current = inputValue; // Save current state
    } else {
      try {
        // Start from current input value
        accumulatedTranscriptRef.current = inputValue || '';
        recognitionRef.current.start();
      } catch (error) {
        console.error('Error starting speech recognition:', error);
        setIsListening(false);
      }
    }
  };

  return (
    <div className="flex items-end border border-gray-300 rounded-lg p-2 bg-white">
      <textarea
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        className="flex-1 border-none focus:outline-none resize-none max-h-32 p-2"
        rows={1}
      />
      <div className="flex items-center ml-2 space-x-1">
        <button
          onClick={toggleListening}
          disabled={disabled}
          className={`p-2 rounded-lg relative group ${
            isListening 
              ? 'bg-red-600 text-white animate-pulse' 
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          } transition-colors`}
          title={isListening ? "Stop recording" : "Speak in English"}
        >
          {isListening ? <X size={18} /> : <Mic size={18} />}
          {/* Tooltip */}
          <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
            {isListening ? "Stop recording" : "Speak in English"}
          </span>
        </button>
        <button
          onClick={handleSubmit}
          disabled={disabled || !inputValue.trim()}
          className={`p-2 rounded-lg ${inputValue.trim() && !disabled ? 'bg-blue-600 text-white' : 'bg-gray-300 text-gray-500'} hover:opacity-90 transition-opacity`}
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
