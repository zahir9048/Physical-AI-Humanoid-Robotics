import React, { useEffect, useState } from 'react';

interface TextSelectionHandlerProps {
  onTextSelected: (selectedText: string, pageUrl: string) => void;
}

const TextSelectionHandler: React.FC<TextSelectionHandlerProps> = ({ onTextSelected }) => {
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const selectedText = selection?.toString().trim() || '';

      if (selectedText) {
        // Only trigger if selection is substantial (more than 5 characters)
        if (selectedText.length > 5) {
          onTextSelected(selectedText, window.location.pathname);
        }
      }
    };

    // Add event listeners for text selection
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    // Cleanup event listeners on unmount
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, [onTextSelected]);

  return null; // This component doesn't render anything
};

export default TextSelectionHandler;