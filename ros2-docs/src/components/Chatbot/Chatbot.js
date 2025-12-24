import React, { useState, useEffect } from 'react'; // Added useEffect
import styles from './Chatbot.module.css';
import { postQuery } from '../../utils/apiClient';
import { getSelectedText } from '../../utils/selectionUtils'; // Import getSelectedText

const Chatbot = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedTextContext, setSelectedTextContext] = useState(''); // New state for selected text

  useEffect(() => {
    const handleSelectionChange = () => {
      const text = getSelectedText();
      setSelectedTextContext(text);
    };

    document.addEventListener('selectionchange', handleSelectionChange);
    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
    };
  }, []);

  const handleSendMessage = async (context = null) => { // Modified to accept context
    const currentInput = input.trim();
    const queryToSend = currentInput || "Tell me more about this."; // Default query if input is empty but context exists
    const contextToSend = context || (selectedTextContext.trim() ? selectedTextContext.trim() : null);

    if (queryToSend || contextToSend) {
      const userMessageText = contextToSend ? `"${contextToSend}" - ${queryToSend}` : queryToSend;
      setMessages((prevMessages) => [...prevMessages, { type: 'user', text: userMessageText }]);
      setInput(''); // Clear input after sending
      setSelectedTextContext(''); // Clear selected text context after sending
      setError(null);
      setIsLoading(true);

      try {
        const response = await postQuery(queryToSend, contextToSend); // Pass context to API
        setMessages((prevMessages) => [...prevMessages, { type: 'bot', text: response.response_text }]);
      } catch (err) {
        console.error("Error fetching chatbot response:", err);
        setError("Failed to get a response from the chatbot. Please try again.");
        setMessages((prevMessages) => [...prevMessages, { type: 'bot', text: "Error: Could not get a response." }]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleAskAboutSelected = () => {
    if (selectedTextContext.trim() && !isLoading) {
      handleSendMessage(selectedTextContext.trim());
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <h3>RAG Chatbot</h3>
      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <p>No messages yet. Ask something!</p>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={styles[msg.type]}>
              {msg.text}
            </div>
          ))
        )}
        {isLoading && <div className={styles.loading}>Thinking...</div>}
        {error && <div className={styles.error}>{error}</div>}
      </div>
      {selectedTextContext.trim() && !isLoading && (
        <div className={styles.selectedContextPrompt}>
          <p>Selected text: "{selectedTextContext.substring(0, 50)}..."</p>
          <button onClick={handleAskAboutSelected}>Ask about selected text</button>
        </div>
      )}
      <div className={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !isLoading) {
              handleSendMessage();
            }
          }}
          placeholder="Ask a question..."
          disabled={isLoading}
        />
        <button onClick={() => handleSendMessage()} disabled={isLoading}>Send</button> {/* Modified */}
      </div>
    </div>
  );
};

export default Chatbot;
