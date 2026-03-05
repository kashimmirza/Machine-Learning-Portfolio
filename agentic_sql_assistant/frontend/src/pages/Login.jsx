import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        try {
            const response = await api.post('/auth/login', formData);
            localStorage.setItem('token', response.data.access_token);
            navigate('/chat');
        } catch (error) {
            console.error(error);
            alert('Login failed');
        }
    };

    return (
        <div className="auth-container">
            <form onSubmit={handleLogin} className="auth-form">
                <h2 style={{ marginTop: 0, textAlign: "center" }}>Agentic SQL Assistant</h2>
                <div className="form-group">
                    <input
                        type="email"
                        placeholder="admin@example.com"
                        className="form-input"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <input
                        type="password"
                        placeholder="Password"
                        className="form-input"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn">
                    Login
                </button>
            </form>
        </div>
    );
}

export default Login;
