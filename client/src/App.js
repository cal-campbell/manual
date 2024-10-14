import React, { useState } from 'react';
import axios from 'axios';
import './App.css';


function App() {
  const [message, setMessage] = useState('');
  const [chatLog, setChatLog] = useState([]);

  const handleSendMessage = async () => {
    if (message.trim()) {
      // Add user message to chat log
      setChatLog([...chatLog, { type: 'user', text: message }]);
      
      // Send message to the backend
      try {
        const response = await axios.post('http://localhost:3000/api/chatbot', { message });
        const botResponse = response.data.response;
        
        // Add bot response to chat log
        setChatLog((prev) => [...prev, { type: 'bot', text: botResponse }]);
      } catch (err) {
        console.error('Error talking to chatbot:', err);
      }
      
      // Clear message input
      setMessage('');
    }
  };

  return (
    <div className="App">
      <h1>Hey Ryan, how can I help you? 😄</h1>
      <div className="chat-window">
        {chatLog.map((entry, index) => (
          <div key={index} className={entry.type === 'user' ? 'user-message' : 'bot-message'}>
            {entry.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
}

export default App;

