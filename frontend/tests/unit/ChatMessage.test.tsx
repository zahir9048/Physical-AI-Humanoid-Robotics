import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ChatMessage from '../../src/components/ChatMessage';
import { Message } from '../../src/services/types';

// Mock the ChatAPI
jest.mock('../../src/services/ChatAPI', () => ({
  submitFeedback: jest.fn().mockResolvedValue({ success: true, message: 'Feedback submitted' }),
}));

// Mock the icons
jest.mock('lucide-react', () => ({
  ThumbsUp: ({ size }: { size: number }) => <span data-testid="thumbs-up" style={{ fontSize: size }}>👍</span>,
  ThumbsDown: ({ size }: { size: number }) => <span data-testid="thumbs-down" style={{ fontSize: size }}>👎</span>,
}));

describe('ChatMessage', () => {
  const mockMessage: Message = {
    id: '1',
    role: 'assistant',
    content: 'This is a test message',
    timestamp: new Date().toISOString(),
    source_chunks: ['chunk-1', 'chunk-2'],
  };

  const mockUserMessage: Message = {
    ...mockMessage,
    role: 'user',
    id: '2',
  };

  const mockAvatar = <span>Avatar</span>;

  it('renders assistant message correctly', () => {
    render(<ChatMessage message={mockMessage} avatar={mockAvatar} />);

    expect(screen.getByText('This is a test message')).toBeInTheDocument();
    expect(screen.getByText('Sources:')).toBeInTheDocument();
    expect(screen.getByText('• chunk-1')).toBeInTheDocument();
  });

  it('renders user message correctly', () => {
    render(<ChatMessage message={mockUserMessage} avatar={mockAvatar} />);

    expect(screen.getByText('This is a test message')).toBeInTheDocument();
    // User messages should not have feedback controls
    expect(screen.queryByTestId('thumbs-up')).not.toBeInTheDocument();
    expect(screen.queryByTestId('thumbs-down')).not.toBeInTheDocument();
  });

  it('shows feedback controls for assistant messages', () => {
    render(<ChatMessage message={mockMessage} avatar={mockAvatar} />);

    expect(screen.getByTestId('thumbs-up')).toBeInTheDocument();
    expect(screen.getByTestId('thumbs-down')).toBeInTheDocument();
  });

  it('allows user to provide feedback', async () => {
    const { ChatAPI } = require('../../src/services/ChatAPI');
    render(<ChatMessage message={mockMessage} avatar={mockAvatar} />);

    // Click thumbs up
    const thumbsUpButton = screen.getByTestId('thumbs-up');
    fireEvent.click(thumbsUpButton);

    // Wait for the async operation to complete
    await new Promise(resolve => setTimeout(resolve, 0));

    // Check if submitFeedback was called
    expect(ChatAPI.submitFeedback).toHaveBeenCalledWith({
      message_id: '1',
      rating: 1,
    });
  });

  it('allows user to provide negative feedback', async () => {
    const { ChatAPI } = require('../../src/services/ChatAPI');
    render(<ChatMessage message={mockMessage} avatar={mockAvatar} />);

    // Click thumbs down
    const thumbsDownButton = screen.getByTestId('thumbs-down');
    fireEvent.click(thumbsDownButton);

    // Wait for the async operation to complete
    await new Promise(resolve => setTimeout(resolve, 0));

    expect(ChatAPI.submitFeedback).toHaveBeenCalledWith({
      message_id: '1',
      rating: -1,
    });
  });
});