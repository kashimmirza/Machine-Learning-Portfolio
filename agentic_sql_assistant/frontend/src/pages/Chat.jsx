import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import api from '../api';

function Chat() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMsg = { role: 'user', content: input };
        setMessages((prev) => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        const token = localStorage.getItem('token');

        // Create a placeholder for the assistant's message
        setMessages((prev) => [...prev, { role: 'assistant', content: '' }]);

        try {
            const response = await fetch('http://localhost:8000/api/v1/chat/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ message: input, session_id: "default" })
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let botContent = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));

                            if (data.content) {
                                botContent += data.content;
                                setMessages((prev) => {
                                    const newMsgs = [...prev];
                                    newMsgs[newMsgs.length - 1] = { role: 'assistant', content: botContent };
                                    return newMsgs;
                                });
                            }
                        } catch (e) {
                            console.error("Error parsing SSE data", e);
                        }
                    }
                }
            }
        } catch (e) {
            console.error("Stream failed", e);
            setMessages((prev) => [...prev, { role: 'assistant', content: "Error: Could not reach the agent." }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <header className="chat-header">
                Agentic SQL Assistant
            </header>

            <div className="messages-area">
                {messages.map((msg, i) => (
                    <div key={i} className={`message ${msg.role}`}>
                        <div className="message-bubble">
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                    </div>
                ))}
                {isLoading && <div style={{ textAlign: 'center', color: '#999' }}>Thinking...</div>}
                <div ref={bottomRef} />
            </div>

            <div className="input-area">
                <input
                    className="chat-input"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Ask a question (e.g., 'Show me top selling products')"
                    disabled={isLoading}
                />
                <button className="btn" style={{ width: 'auto' }} onClick={sendMessage} disabled={isLoading}>
                    Send
                </button>
            </div>
        </div>
    );
}

export default Chat;
