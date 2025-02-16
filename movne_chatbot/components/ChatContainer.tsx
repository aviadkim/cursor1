import styled from 'styled-components';

export const ChatContainer = styled.div`
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 20px;
  margin: 10px;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  }
`; 