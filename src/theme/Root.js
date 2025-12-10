import React, { useState } from 'react';
import ChatWidget from '../components/Chatbot/ChatWidget';
import TextSelectionHandler from '../components/Chatbot/TextSelectionHandler';

// Default implementation, that you can customize
export default function Root({children}) {
  const [selectedText, setSelectedText] = useState('');
  const [pageUrl, setPageUrl] = useState('');

  const handleTextSelected = (text, url) => {
    setSelectedText(text);
    setPageUrl(url);
  };

  return (
    <>
      {children}
      <TextSelectionHandler onTextSelected={handleTextSelected} />
      <ChatWidget initialSelectedText={selectedText} initialPageUrl={pageUrl} />
    </>
  );
}
