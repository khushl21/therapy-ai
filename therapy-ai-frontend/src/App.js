import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');

    // Format messages for backend
    const formattedPrompt = newMessages
      .map(m => `${m.role === 'user' ? 'User' : 'Therapist'}: ${m.content}`)
      .join('\n') + '\nTherapist:';

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        prompt: formattedPrompt
      });

      const reply = response.data.reply;
      const botMessage = { role: 'therapist', content: reply };
      setMessages([...newMessages, botMessage]);
    } catch (error) {
      console.error("API error:", error);
    }
  };

  return (
    <div className="app-container">
      <h1>Therapy AI</h1>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={msg.role === 'user' ? 'user-msg' : 'bot-msg'}
          >
            {msg.content}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          placeholder="How are you feeling today?"
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default App;
