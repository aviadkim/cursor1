import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';

const ChatContainer = styled.div`
  width: 400px;
  height: 600px;
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Assistant', sans-serif;
`;

const ChatHeader = styled.div`
  padding: 20px;
  background: rgba(255,255,255,0.05);
  display: flex;
  align-items: center;
  gap: 10px;
`;

const Logo = styled.img`
  width: 30px;
  height: 30px;
`;

const Title = styled.h2`
  color: #fff;
  margin: 0;
  font-weight: 500;
  font-size: 1.1rem;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.2);
    border-radius: 3px;
  }
`;

const Message = styled.div<{ isBot?: boolean }>`
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 15px;
  color: #fff;
  align-self: ${props => props.isBot ? 'flex-start' : 'flex-end'};
  background: ${props => props.isBot ? 'rgba(255,255,255,0.1)' : '#0066ff'};
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    bottom: 0;
    ${props => props.isBot ? 'left: -7px' : 'right: -7px'};
    width: 15px;
    height: 15px;
    background: ${props => props.isBot ? 'rgba(255,255,255,0.1)' : '#0066ff'};
    clip-path: polygon(0 0, 100% 100%, 100% 0);
    transform: ${props => props.isBot ? 'rotate(45deg)' : 'rotate(-45deg)'};
  }
`;

const InputContainer = styled.div`
  padding: 20px;
  background: rgba(255,255,255,0.05);
  display: flex;
  gap: 10px;
`;

const Input = styled.input`
  flex: 1;
  padding: 12px 16px;
  border-radius: 25px;
  border: none;
  background: rgba(255,255,255,0.1);
  color: #fff;
  font-size: 0.9rem;
  
  &::placeholder {
    color: rgba(255,255,255,0.5);
  }
  
  &:focus {
    outline: none;
    background: rgba(255,255,255,0.15);
  }
`;

const SendButton = styled.button`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #0066ff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 0.2s;
  
  &:hover {
    transform: scale(1.05);
    background: #0052cc;
  }
`;

const SystemStatus = styled.div<{ isError?: boolean }>`
  padding: 10px;
  margin: 10px;
  border-radius: 8px;
  background: ${props => props.isError ? 'rgba(255,0,0,0.1)' : 'rgba(0,255,0,0.1)'};
  color: #fff;
  font-size: 0.9rem;
  display: ${props => props.isError ? 'block' : 'none'};
`;

const CheckSystemButton = styled.button`
  padding: 8px 16px;
  background: rgba(255,255,255,0.1);
  border: none;
  border-radius: 15px;
  color: #fff;
  cursor: pointer;
  font-size: 0.9rem;
  margin: 10px;
  
  &:hover {
    background: rgba(255,255,255,0.2);
  }
`;

interface Message {
  id: string;
  text: string;
  isBot: boolean;
}

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState<string>('');
  const [isError, setIsError] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      isBot: false
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json; charset=utf-8'
        },
        body: JSON.stringify({
          query: input,
          user_id: 'USER_ID' // יש להחליף ב-ID אמיתי
        })
      });

      const data = await response.json();

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: decodeURIComponent(escape(data.response)),
        isBot: true
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const checkSystem = async () => {
    setIsLoading(true);
    setSystemStatus('בודק את המערכת...');
    setIsError(false);

    try {
      // בדיקת שרת Flask
      const flaskResponse = await fetch('http://127.0.0.1:5000/health', {
        method: 'GET'
      });
      
      if (!flaskResponse.ok) {
        throw new Error('שרת Flask לא מגיב');
      }

      // בדיקת חיבור ל-OpenAI
      const openaiResponse = await fetch('http://127.0.0.1:5000/test-openai', {
        method: 'GET'
      });

      if (!openaiResponse.ok) {
        throw new Error('בעיה בחיבור ל-OpenAI');
      }

      setSystemStatus('כל המערכות פועלות כראוי');
      setIsError(false);
    } catch (error: any) {
      setSystemStatus(`שגיאת מערכת: ${error.message}`);
      setIsError(true);
      console.error('System check error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChatContainer>
      <ChatHeader>
        <Title>Movne Global Assistant</Title>
        <CheckSystemButton onClick={checkSystem}>
          בדיקת מערכת
        </CheckSystemButton>
      </ChatHeader>
      
      <SystemStatus isError={isError}>
        {systemStatus}
      </SystemStatus>
      
      <MessagesContainer>
        {messages.map(message => (
          <Message key={message.id} isBot={message.isBot}>
            {message.text}
          </Message>
        ))}
        <div ref={messagesEndRef} />
      </MessagesContainer>
      
      <InputContainer>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="שאל/י שאלה..."
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <SendButton onClick={handleSend}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </SendButton>
      </InputContainer>
    </ChatContainer>
  );
}; 