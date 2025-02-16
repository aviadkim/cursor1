import styled, { keyframes } from 'styled-components';
import { ChatContainer } from './ChatContainer';

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const typing = keyframes`
  0% { opacity: 0.3; }
  50% { opacity: 1; }
  100% { opacity: 0.3; }
`;

export const TypingIndicator = styled.div`
  display: flex;
  gap: 5px;
  padding: 12px 16px;
  background: rgba(255,255,255,0.1);
  border-radius: 15px;
  width: fit-content;
  margin: 10px 0;
`;

export const Dot = styled.div`
  width: 6px;
  height: 6px;
  background: #fff;
  border-radius: 50%;
  animation: ${typing} 1s infinite;
  
  &:nth-child(2) {
    animation-delay: 0.2s;
  }
  
  &:nth-child(3) {
    animation-delay: 0.4s;
  }
`;

export const AnimatedMessage = styled.div<{ isBot?: boolean }>`
  animation: ${fadeIn} 0.3s ease-out;
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
    background: inherit;
    clip-path: polygon(0 0, 100% 100%, 100% 0);
    transform: ${props => props.isBot ? 'rotate(45deg)' : 'rotate(-45deg)'};
  }
`;

export const GlowEffect = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 50% 50%, rgba(0,102,255,0.1) 0%, transparent 70%);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
  
  ${() => ChatContainer}:hover & {
    opacity: 1;
  }
`; 